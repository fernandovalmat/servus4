from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField
from data.models import Centro, Productos, Proveedor
from django.db import models
from django.db.models.fields.related import ForeignKey

class Remitos(models.Model): #ingreso
    tipos=[('I','ingreso'),('E', 'egreso'),('T', 'transferencia')]
    idremito=models.AutoField(primary_key=True)
    origen=models.ForeignKey(Proveedor, on_delete=CASCADE) #FK
    destino=models.ForeignKey(Centro, on_delete=CASCADE) #FK
    fecha_remito=models.DateField(default=datetime.now)
    tipo=models.CharField(choices=tipos, default=0, max_length=15)
    ajuste=models.BooleanField(default=False)
    costo=models.IntegerField(default=0)
    
    def __str__(self):
        return '%s'% self.idremito
    
class Renglones(models.Model): #ingreso
    nremito=models.ManyToManyField(Remitos) #FK
    idrenglon=models.AutoField(primary_key=True)
    producto=models.ForeignKey(Productos, on_delete=CASCADE) #FK
    cantidad=models.FloatField(default=0)
    costo=models.IntegerField(default=0)
    def __str__(self):
        return '%s,%s,%s,%s' % (self.nremito, self.idrenglon, self.producto, self.cantidad)

# class Costo(models.Model):
#     nremito=models.ForeignKey(Remitos, on_delete=CASCADE)
#     costo=models.IntegerField(default=0)