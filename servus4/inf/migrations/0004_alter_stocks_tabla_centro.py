# Generated by Django 3.2.3 on 2021-11-11 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
        ('inf', '0003_alter_stocks_tabla_centro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks_tabla',
            name='centro',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='data.centro'),
        ),
    ]
