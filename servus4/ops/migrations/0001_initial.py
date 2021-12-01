# Generated by Django 3.2.3 on 2021-11-07 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remitos',
            fields=[
                ('idremito', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_remito', models.DateField()),
                ('tipo', models.CharField(choices=[('I', 'ingreso'), ('E', 'egreso'), ('T', 'transferencia')], default=0, max_length=15)),
                ('ajuste', models.BooleanField(default=False)),
                ('destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.centro')),
                ('origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Renglones',
            fields=[
                ('idrenglon', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.FloatField()),
                ('nremito', models.ManyToManyField(to='ops.Remitos')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.productos')),
            ],
        ),
    ]
