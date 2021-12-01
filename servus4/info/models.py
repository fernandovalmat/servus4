from django.db import models


from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from data.models import Centro, Productos, Proveedor

class Totales2(models.Model): 
	centro=models.ForeignKey(Centro, on_delete=CASCADE)
	producto=models.ForeignKey(Productos, on_delete=CASCADE)
	cantidad=models.IntegerField()
	costo=models.IntegerField()
	
class Consumos_mensuales2(models.Model): #es para los centros
	centro=models.ForeignKey(Centro, on_delete=CASCADE)
	producto=models.ForeignKey(Productos, on_delete=CASCADE)
	cantidad=models.IntegerField(default=0)
	costo=models.FloatField(default=0, null=True)
	promedio=models.FloatField(default=0, null=True)
	costopromedio=models.FloatField(default=0, null=True)
	anio=models.IntegerField(default=2021, null=True)
	mes=models.IntegerField(default=1, null=True)

class Consumos_totales2(models.Model):
	centro=models.ForeignKey(Centro, on_delete=CASCADE)
	producto=models.ForeignKey(Productos, on_delete=CASCADE)
	cantidad=models.FloatField(default=0)
	costo=models.FloatField(default=0, null=True)
	promedio=models.FloatField(default=0, null=True)
	def __str__(self):
		return '%s' % (self.producto)

class Stocks_tabla2(models.Model):
	producto=models.ForeignKey(Productos, on_delete=CASCADE)
	stock_umaad=models.IntegerField(default=0, null=True)
	stock_nck=models.IntegerField(default=0, null=True)
	ingreso_umaad=models.IntegerField(default=0, null=True)
	egreso_umaad=models.IntegerField(default=0, null=True)
	ingreso_nck=models.IntegerField(default=0, null=True)
	egreso_nck=models.IntegerField(default=0, null=True)
	duracion_umaad=models.FloatField(default=0, null=True)
	duracion_nck=models.FloatField(default=0, null=True)
	promedio_umaad=IntegerField(default=0, null=True)
	promedio_nck=models.IntegerField(default=0, null=True)

class Ies(models.Model):
	centro=models.ForeignKey(Centro, on_delete=CASCADE)
	producto=models.ForeignKey(Productos, on_delete=CASCADE)
	ingreso=models.IntegerField(default=0, null=True)
	egreso=models.IntegerField(default=0, null=True)
	stock=models.IntegerField(default=0, null=True)

class Consumos_mensual_1(models.Model): #es para los nck y umaad
	centro=models.ForeignKey(Proveedor, on_delete=CASCADE)
	producto=models.ForeignKey(Productos, on_delete=CASCADE)
	cantidad=models.IntegerField(default=0)
	costo=models.FloatField(default=0, null=True)
	promedio=models.FloatField(default=0, null=True)
	costopromedio=models.FloatField(default=0, null=True)
	anio=models.IntegerField(default=2021, null=True)
	mes=models.IntegerField(default=1, null=True)