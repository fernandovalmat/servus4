
from django.db import models
from django.db.models.deletion import CASCADE
from data.models import Centro, Productos

class Totales(models.Model): 
	centro=models.ForeignKey(Centro, on_delete=CASCADE)
	producto=models.ForeignKey(Productos, on_delete=CASCADE)
	cantidad=models.IntegerField()
	costo=models.IntegerField()
	
class Consumos_mensuales(models.Model):
	centro=models.ForeignKey(Centro, on_delete=CASCADE)
	producto=models.ForeignKey(Productos, on_delete=CASCADE)
	cantidad=models.IntegerField(default=0)
	fecha=models.DateField(default='2021-01-01') 
	costo=models.FloatField(default=0, null=True)
	promedio=models.FloatField(default=0, null=True)
	costopromedio=models.FloatField(default=0, null=True)

class Consumos_totales(models.Model):
	centro=models.ForeignKey(Centro, on_delete=CASCADE)
	producto=models.ForeignKey(Productos, on_delete=CASCADE)
	cantidad=models.FloatField(default=0)
	costo=models.FloatField(default=0, null=True)
	promedio=models.FloatField(default=0, null=True)
	def __str__(self):
		return '%s' % (self.producto)


class Stocks_tabla(models.Model):
	producto=models.ForeignKey(Productos, on_delete=CASCADE)
	stock_umaad=models.IntegerField(default=0, null=True)
	stock_nck=models.IntegerField(default=0, null=True)
	ingreso_umaad=models.IntegerField(default=0, null=True)
	egreso_umaad=models.IntegerField(default=0, null=True)
	ingreso_nck=models.IntegerField(default=0, null=True)
	egreso_nck=models.IntegerField(default=0, null=True)
	

