# Generated by Django 3.2.3 on 2021-11-24 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0004_alter_remitos_fecha_remito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renglones',
            name='cantidad',
            field=models.FloatField(default=0),
        ),
    ]