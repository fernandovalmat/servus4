# Generated by Django 3.2.3 on 2021-11-23 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_auto_20211117_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks_tabla2',
            name='promedio_nck',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='stocks_tabla2',
            name='promedio_umaad',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
