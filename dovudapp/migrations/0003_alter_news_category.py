# Generated by Django 4.2 on 2023-04-08 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dovudapp', '0002_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dovudapp.category'),
        ),
    ]
