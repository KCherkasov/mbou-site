# Generated by Django 2.0.6 on 2020-01-26 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mbou', '0018_news_doc_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='pic',
            field=models.FileField(blank=True, upload_to='pics'),
        ),
    ]
