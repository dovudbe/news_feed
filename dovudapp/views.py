from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import News,Category
from .forms import ContactForm, CommentForm
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from project.costum_permision import OnlyLoggedSuperUser
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from hitcount.utils import get_hitcount_model

def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published)

    context = {
        'news_list':news_list  
    }

    return render(request, "news/news_list.html", context)


from hitcount.views import HitCountDetailView, HitCountMixin


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)

    context = {}

    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk':hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1

        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits


    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        'news':news,
        'comments':comments,
        'new_comment':new_comment,
        'comment_form':comment_form,
        'comment_count': comment_count,
    }

    return render(request, 'news/news_detail.html', context)

def HomePageView(request):
    categories = Category.objects.all()
    news_list = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[:5]
    mahalliy_xabarlar = News.objects.filter(status=News.Status.Published, category__name='Mahalliy').order_by('-publish_time')[:5]
    horij_xabarlari = News.objects.filter(status=News.Status.Published, category__name='Xorij').order_by('-publish_time')[:5]
    sport_xabarlari = News.objects.filter(status=News.Status.Published, category__name='Sport').order_by('-publish_time')[:5]
    texnologik_xabarlar = News.objects.filter(status=News.Status.Published, category__name='Texnologiya').order_by('-publish_time')[:5]
    context = {
        'news_list':news_list,
        'categories':categories,
        'mahalliy_xabarlar':mahalliy_xabarlar,
        'sport_xabarlari':sport_xabarlari,
        'horij_xabarlari': horij_xabarlari,
        'texnologik_xabarlar':texnologik_xabarlar,
    }

    return render(request, 'news/home.html', context)


def ContactPageView(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponse("<h2> biz bilan bog'langaningiz uchun rahmat ? </h2>")
    context = {

        "form":form

    }

    return render(request, 'news/contact.html', context)


def AboutPageView(request):
    context = {

    }

    return render(request, 'news/ebout.html', context)


def ErrorPageView(request):
    context = {

    }

    return render(request, 'news/404.html', context)

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def queryset(self):
        news = News.objects.filter(status=News.Status.Published, category__name='Xorij')
        return news

class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologik_yangiliklar'

    def queryset(self):
        news = News.objects.filter(status=News.Status.Published, category__name='Texnologiya')
        return news

class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklari'

    def queryset(self):
        news = News.objects.filter(status=News.Status.Published, category__name='Sport')
        return news

class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def queryset(self):
        news = News.objects.filter(status=News.Status.Published, category__name='Mahalliy')

        return news



class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'slug', 'body', 'imagess', 'category','status')
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser , DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'title_uz', 'title_en', 'title_ru',
              'slug','body', 'body_uz', 'body_en', 
              'body_ru', 'imagess','category', 'status')


@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users':admin_users
    }

    return render(request, 'pages/admin_page.html', context)


class SearchResultList(ListView):

    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'


def get_queryset(self):
    query = self.request.GET.get('q')
    return News.objects.filter(
        Q(title__icontains = query) | Q(body__icontains = query)
    )