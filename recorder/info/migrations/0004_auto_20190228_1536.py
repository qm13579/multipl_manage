# Generated by Django 2.1.4 on 2019-02-28 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_auto_20190102_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlinfo',
            name='key',
            field=models.CharField(blank=True, max_length=248, null=True, verbose_name='提取关键词'),
        ),
    ]