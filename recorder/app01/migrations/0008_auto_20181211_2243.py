# Generated by Django 2.1 on 2018-12-11 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_auto_20181211_2227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('app01_table_list', '可以查看kingadmin中的所有数据'), ('app01_table_list_view', '可以查看kingadmin中每条数据的修改页'), ('app01_table_list_change', '可以查看kingadmin中每条数据进行修改'), ('app01_table_list_add_view', '可以查看kingadmin中每张表增加页'), ('app01_table_list_add', '可以查看kingadmin中的进行数据增加'))},
        ),
    ]