# Generated by Django 2.1 on 2018-11-26 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_detailed_detai'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailed',
            name='file_stores_id',
            field=models.ForeignKey(on_delete='CASCADE', to='app01.FileStore'),
        ),
    ]
