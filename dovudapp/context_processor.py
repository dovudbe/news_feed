from .models import News

def latest_news(request):
    latest_news = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[:10]

    context = {
        'latest_news':latest_news
    }

    return context