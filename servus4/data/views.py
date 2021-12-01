from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, request



from .forms import *


def home_data(request):
    return render(request, 'data_app/home_data.html')

class Agregar_centro(HttpRequest):
    def agregar_centro(request):
        centro=Centro_form()
        centros=Centro.objects.all()
        return render(request, 'data_app/agregar_centro.html', {'centro':centro, 'centros':centros})
    def guardar_centro(request):
        centro=Centro_form(request.POST)
        if centro.is_valid():
            centro.save()
        centro=Centro_form()
        centros=Centro.objects.all()
        return render(request, 'data_app/agregar_centro.html', {'centro':centro, 'centros':centros})
    def borrar_centro(request):
        centros=Centro.objects.all()
        centro_seleccionado=request.POST.get('centro')
        if request.method=='POST':
            centro=centro_seleccionado
            Centro.objects.filter(idcentro=centro_seleccionado).delete()    
        return render(request, 'data_app/editar_centro.html', {'centros':centros})

class Productos_edit(HttpRequest):
    def agregar_producto(request):
        producto=Productos_form()
        productos=Productos.objects.all().order_by('nombre_producto')
        
        return render(request, 'data_app/agregar_producto.html', {'producto':producto, 'productos':productos})
    
    def guardar_producto(request):
        producto=Productos_form(request.POST)
        if producto.is_valid():
            producto.save()
        producto=Productos_form()
        productos=Productos.objects.all()
        
        return render(request, 'data_app/agregar_producto.html', {'producto':producto, 'productos':productos})
    
    def borrar_producto(request):
        productos=Productos.objects.all().order_by('nombre_producto')
        producto_seleccionado=request.POST.get('producto')
        if request.method=='POST':
            producto=producto_seleccionado
        Productos.objects.filter(idproductos=producto_seleccionado).delete()
        return render(request, 'data_app/borrar_producto.html', {'productos':productos})
    
    def actualizar_precios(request):
        prod=Productos.objects.all()
        idproducto=request.POST.get('idproducto')
        nuevo_precio=request.POST.get('nuevo_precio')
        Productos.objects.filter(idproductos=idproducto).update(precio=nuevo_precio)

        return render(request, 'data_app/actualizar_precio.html', {'prod':prod})

    def lista_productos(request):
        med=Productos.objects.filter(categoria='m').order_by('nombre_producto')
        des=Productos.objects.filter(categoria='d').order_by('nombre_producto')
        alimentos=Productos.objects.filter(categoria='al').order_by('nombre_producto')
        otros=Productos.objects.filter(categoria='o').order_by('nombre_producto')
        soluciones=Productos.objects.filter(categoria='s').order_by('nombre_producto')

        return render(request,'data_app/lista_productos.html', {'med':med, 'des':des, 'alimentos':alimentos, 'otros':otros, 'soluciones':soluciones})

class Proveedores_edit(HttpRequest):
    def agregar_proveedor(request):
        proveedor=Proveedores_form()
        proveedores=Proveedor.objects.all()
        return render(request, 'data_app/agregar_proveedor.html', {'proveedor':proveedor, 'proveedores':proveedores})

    def guardar_proveedor(request):
        proveedor=Proveedores_form(request.POST)
        if proveedor.is_valid():
            proveedor.save()
        proveedor=Proveedores_form()
        proveedores=Proveedor.objects.all()
        return render(request, 'data_app/agregar_proveedor.html', {'proveedor':proveedor, 'proveedores':proveedores})
        
    def borrar_proveedor(request):
        proveedores=Proveedor.objects.all()
        proveedor_seleccionado=request.POST.get('proveedor')
        if request.method=='POST':
            proveedor=proveedor_seleccionado
        Proveedor.objects.filter(idproveedor=proveedor_seleccionado).delete()
        return render(request, 'data_app/borrar_proveedor.html', {'proveedores':proveedores})

# Create your views here.
