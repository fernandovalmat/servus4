# Generated by Django 3.2.3 on 2021-11-11 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
        ('inf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks_tabla',
            name='centro',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='data.centro'),
        ),
        migrations.AddField(
            model_name='stocks_tabla',
            name='stock_centro',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
