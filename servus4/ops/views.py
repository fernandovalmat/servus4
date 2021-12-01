from datetime import datetime
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.db.models import Sum, Avg
from django.core.paginator import Paginator
from data.models import Productos
from .models import Remitos, Renglones
from .forms import Remitos_form, Renglones_form

# Create your views here.
def home_ops(request):
    return render(request, 'home_ops.html')

class Operaciones(HttpRequest): #OK todo
    def crear_remito(request):
        nuevo_remito=Remitos_form()
        datos_remito=Remitos_form(request.POST)
        if datos_remito.is_valid():
            datos_remito.save()
            datos_remito.clean()
        
        idr=request.POST.get('idr')
        if request.method=='POST':
            idr=idr
            q=Remitos.objects.filter(idremito=idr).exists()
            if q== True:
                remito=Remitos.objects.get(idremito=idr)
                costo=Renglones.objects.filter(nremito=remito).aggregate(Sum('costo'))
                cost=sum(costo.values())
                Remitos.objects.filter(idremito=idr).update(costo=cost)
            else:
                pass
        
        remitos=Remitos.objects.all().order_by('-idremito').exclude(ajuste=True) 

        return render (request, 'ops/operaciones.html', {'nuevo_remito':nuevo_remito, 'remitos':remitos})
    
    def edicion_dinamica(request, id): #ok
        remito=Remitos.objects.get(idremito=id)

        nuevo_renglon=Renglones_form(initial={'nremito':id})
        if request.method == 'POST':
            nuevo_renglon = Renglones_form(request.POST)
        
            if nuevo_renglon.is_valid():
                data=nuevo_renglon.cleaned_data
                nremito=nuevo_renglon.cleaned_data['nremito']
                producto=nuevo_renglon.cleaned_data['producto']
                cantidad=nuevo_renglon.cleaned_data['cantidad']
                nuevo_renglon=Renglones(producto=producto, cantidad=cantidad)
                nuevo_renglon.save()
                nuevo_renglon.nremito.add(id)
                nuevo_renglon=Renglones_form(initial={'nremito':id})
                renglones=Renglones.objects.filter(nremito=id)
                nrenglones=len(renglones)
                idrenglones=list(renglones.values_list('idrenglon', flat=True))

                c=0
                while c < nrenglones:
                    try:
                        for i in idrenglones: 
                            renglon_prod=list(Renglones.objects.filter(idrenglon=i).values_list('producto', flat=True))
                            precio_prod=Productos.objects.filter(idproductos=renglon_prod[0]).aggregate(Sum('precio'))
                            renglon_cant=Renglones.objects.filter(idrenglon=i).aggregate(Sum('cantidad'))
                            cc=sum(precio_prod.values())*sum(renglon_cant.values())
                            Renglones.objects.filter(idrenglon=i).update(costo=cc)
                            c=c+1
                        
                    except:
                        c=c+1
                        continue

        
        #borrar
        id_borrar=request.POST.get('borrar')
        if request.method=='POST':
            id_borrar=id_borrar
        borrar=Renglones.objects.filter(idrenglon=id_borrar).delete()
        nuevo_renglon=Renglones_form(initial={'nremito':id})

        #actualizar cantidad
        idre2=request.POST.get('actualizar')
        ncantidad=request.POST.get('ncantidad')
        if request.method=='POST':
            idre2=idre2
            ncantidad=ncantidad
        update=Renglones.objects.filter(idrenglon=idre2).update(cantidad=ncantidad)
        add=Renglones_form()

        renglones=Renglones.objects.filter(nremito=id)
        nrenglones=len(renglones)
        idrenglones=list(renglones.values_list('idrenglon', flat=True))

        calcular=request.POST.get('calcular')
        if request.method=='POST':

            c=0
            while c < nrenglones:
                try:
                    for i in idrenglones: 
                        renglon_prod=list(Renglones.objects.filter(idrenglon=i).values_list('producto', flat=True))
                        precio_prod=Productos.objects.filter(idproductos=renglon_prod[0]).aggregate(Sum('precio'))
                        renglon_cant=Renglones.objects.filter(idrenglon=i).aggregate(Sum('cantidad'))
                        cc=sum(precio_prod.values())*sum(renglon_cant.values())
                        Renglones.objects.filter(idrenglon=i).update(costo=cc)
                        c=c+1
                        
                except:
                    c=c+1
                    continue

        return render (request, 'ops/edicion_dinamica.html', {'remito':remito, 'nuevo_renglon':nuevo_renglon, 'id':id, 'renglones':renglones, 'idrenglones':idrenglones})
    




















    def vd_remito_terminado(request, id):
        remito=Remitos.objects.all().filter(idremito=id)
        renglones=Renglones.objects.all().filter(nremito=id)
        return render (request, 'ops/vd_remito_terminado.html', {'remito':remito, 'renglones':renglones})