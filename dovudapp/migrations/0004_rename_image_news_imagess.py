# Generated by Django 4.2 on 2023-04-08 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dovudapp', '0003_alter_news_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='image',
            new_name='imagess',
        ),
    ]
