# Generated by Django 3.2.3 on 2021-11-17 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inf', '0016_stocks_tabla_centro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stocks_tabla',
            name='centro',
        ),
    ]
