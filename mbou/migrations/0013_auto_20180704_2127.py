# Generated by Django 2.0.6 on 2018-07-04 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mbou', '0012_auto_20180618_1825'),
    ]

    operations = [
        migrations.CreateModel(
            name='StafferCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('middle_name', models.TextField()),
                ('last_name', models.TextField()),
                ('is_chairman', models.BooleanField(default=False)),
                ('chair_position', models.TextField(default='')),
                ('is_combiner', models.BooleanField(default=False)),
                ('email', models.EmailField(default='', max_length=254)),
                ('experience', models.IntegerField(default=0)),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='mbou.StafferCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='staffmember',
            name='subject',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='mbou.Subject'),
        ),
    ]