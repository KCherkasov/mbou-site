# Generated by Django 2.0.6 on 2018-07-13 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mbou', '0016_urluser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='photos_count',
        ),
    ]
