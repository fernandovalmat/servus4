# Generated by Django 3.2.3 on 2021-11-17 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Totales2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('costo', models.IntegerField()),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.centro')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.productos')),
            ],
        ),
        migrations.CreateModel(
            name='Stocks_tabla2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_umaad', models.IntegerField(default=0, null=True)),
                ('stock_nck', models.IntegerField(default=0, null=True)),
                ('ingreso_umaad', models.IntegerField(default=0, null=True)),
                ('egreso_umaad', models.IntegerField(default=0, null=True)),
                ('ingreso_nck', models.IntegerField(default=0, null=True)),
                ('egreso_nck', models.IntegerField(default=0, null=True)),
                ('duracion_umaad', models.IntegerField()),
                ('duracion_nck', models.IntegerField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.productos')),
            ],
        ),
        migrations.CreateModel(
            name='Consumos_totales2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField(default=0)),
                ('costo', models.FloatField(default=0, null=True)),
                ('promedio', models.FloatField(default=0, null=True)),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.centro')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.productos')),
            ],
        ),
        migrations.CreateModel(
            name='Consumos_mensuales2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('fecha', models.DateField(default='2021-01-01')),
                ('costo', models.FloatField(default=0, null=True)),
                ('promedio', models.FloatField(default=0, null=True)),
                ('costopromedio', models.FloatField(default=0, null=True)),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.centro')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.productos')),
            ],
        ),
    ]
