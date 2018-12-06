# Generated by Django 2.1 on 2018-12-04 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20181203_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filestore',
            name='file_format',
            field=models.SmallIntegerField(choices=[(0, 'xls'), (1, 'csv'), (2, 'json'), (3, 'txt')], default=0, verbose_name='文件格式'),
        ),
    ]