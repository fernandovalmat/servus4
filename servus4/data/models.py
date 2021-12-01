from django.db import models

# Create your models here.
from django.db import models
from django.db.models.fields import AutoField

from django.db.models.deletion import CASCADE

class Centro(models.Model):
    idcentro=models.AutoField(primary_key=True)
    nombre_centro=models.CharField(max_length=25)
    area=models.CharField(max_length=25, blank=True) #model choices?
    direccion=models.CharField(max_length=30, blank=True)
    def __str__(self):
        return '%s %s %s %s' % (self.nombre_centro,self.idcentro,  self.area, self.direccion)


class Proveedor(models.Model):
    idproveedor=models.AutoField(primary_key=True)
    nombre_proveedor=models.CharField(max_length=25)
    otros_datos=models.CharField(max_length=50, blank=True)
    def __str__(self):
        return '%s %s' % (self.nombre_proveedor, self.idproveedor)


class Productos(models.Model):
    categorias_opciones=[
        ('m', 'Medicamento'), 
        ('d', 'Descartables'), 
        ('s','Soluciones'), 
        ('al', 'Alimentos'),
        ('o', 'Otros')]
    idproductos=models.AutoField(primary_key=True)
    nombre_producto=models.CharField(max_length=50)
    categoria=models.CharField(max_length=20, blank=True, choices=categorias_opciones)
    subcategoria=models.CharField(max_length=15, blank=True)
    precio=models.FloatField(blank=True, null=True)
    alias=models.CharField(max_length=30, blank=True)
    detalle=models.CharField(max_length=100, blank=True)
    stock_critico=models.FloatField(blank=True, null=True)
    stock_disponible=models.IntegerField(blank=True, null=True, default=0)
    egreso=models.IntegerField(null=True, blank=True, default=0)
    ingreso=models.IntegerField(null=True, blank=True, default=0)
    def __str__(self):
        return '%s' % (self.nombre_producto)

