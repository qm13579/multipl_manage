# Generated by Django 2.1 on 2019-01-02 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_auto_20181220_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinfo',
            name='keyword_1',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='关键词1'),
        ),
        migrations.AddField(
            model_name='webinfo',
            name='keyword_2',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='关键词2'),
        ),
        migrations.AddField(
            model_name='webinfo',
            name='keyword_3',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='关键词3'),
        ),
        migrations.AddField(
            model_name='webinfo',
            name='keyword_4',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='关键词4'),
        ),
        migrations.AddField(
            model_name='webinfo',
            name='keyword_5',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='关键词5'),
        ),
    ]
