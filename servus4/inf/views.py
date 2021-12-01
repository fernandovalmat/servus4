# from datetime import datetime
# from django.db.models.query import QuerySet
# from django.http.request import HttpRequest
# from django.shortcuts import render
# from django.db.models import Sum, Avg
# from data.models import *
# from ops.models import *
# from .models import Consumos_mensuales, Consumos_totales, Totales, Stocks_tabla
# from django.utils import timezone

# #IMPORTANTE
# #CREAR FUNCIONES DE ACTUALIZACION DE TODAS LAS TABLAS.
# #VER SI SE PUEDE HACER ALGO QUE ACTUALICE CUANDO ESTA EN ONLINE A DETERMINADA HORA.



# def estadisticas_home(request):
#     return render (request, 'home.html')

# class Stock(HttpRequest):

#     def consumo_total(request): 
        
#         producto=Productos.objects.all().order_by('nombre_producto')
#         consumo=Stocks_tabla.objects.all().order_by('producto')
#         umaad=Proveedor.objects.get(nombre_proveedor='UMAAD')
#         umad=Centro.objects.get(nombre_centro='UMAAD')
#         c=0
#         while c<5:
#             for idproducto in range(1,500):
#                 try:
#                     suma_ingreso_producto=Renglones.objects.filter(nremito__in=Remitos.objects.filter(destino=umad).exclude(ajuste=True)).filter(producto=idproducto).aggregate(total_eg=Sum('cantidad'))
#                     ingreso_t=sum(suma_ingreso_producto.values())
                    
#                     #Productos.objects.filter(idproductos=idproducto).update(ingreso=ingreso_t)
#                     Stocks_tabla.objects.filter(producto=idproducto).update(ingreso_umaad=ingreso_t)
#                 except TypeError:
                    
#                     #Productos.objects.filter(idproductos=idproducto).update(ingreso=0)
#                     Stocks_tabla.objects.filter(producto=idproducto).update(ingreso_umaad=0)
#                     c=c+1
#                     continue
#         c=0
#         while c<5:
#             for idproducto in range(1,500):
#                 try:
#                     suma_egreso_producto=Renglones.objects.filter(nremito__in=Remitos.objects.filter(origen=umaad).exclude(ajuste=True)).filter(producto=idproducto).aggregate(total_eg=Sum('cantidad'))
#                     egreso_t=sum(suma_egreso_producto.values())
                 
#                     Stocks_tabla.objects.filter(producto=idproducto).update(egreso_umaad=egreso_t)
#                 except TypeError:
                    
#                     Stocks_tabla.objects.filter(producto=idproducto).update(egreso_umaad=0)
#                     c=c+1
#                     continue
                
#         return render (request, 'inf/consumo_total.html', {'consumo':consumo})
    
#     def ciclico_stock(request, id): 
#         #generar proveedor ajuste
#         stock=Stocks_tabla.objects.filter(producto=id)
       
#         sd1=request.POST.get('sd1')
#         nc=request.POST.get('nc')
#         evaluador=0
#         ajuste_ingreso=Proveedor.objects.get(nombre_proveedor='ajustes') #umaad: 6
#         ajuste_egreso=Centro.objects.get(nombre_centro='ajustes') #umaad:9
#         #en rigor puede ser un solo objeto que recibe o entrega
#         umaad_proveedor=Proveedor.objects.get(nombre_proveedor='UMAAD')
#         umaad_centro=Centro.objects.get(nombre_centro='UMAAD') #umaad:9
        
#         producto=Productos.objects.get(idproductos=id)
#         if request.method=='POST': 
            
#             evaluador=int(sd1)-int(nc) #stock - recuento

#             if int(sd1)<0 and int(nc)==0: #ingresa insumo DESDE AJUSTE INGRESO QUE ES EL PROVEEDOR
#                 r=Remitos(tipo='I', origen=ajuste_ingreso, destino=umaad_centro, fecha_remito=datetime.now(), ajuste=True)
#                 r.save()
#                 re=Renglones(producto=producto, cantidad=-int(sd1))
#                 re.save()
#                 re.nremito.add(r)
            
#             if int(sd1)> 0 and int(nc)==0: #egresa insumo , FUNCIONA
#                 r=Remitos(tipo='E', origen=umaad_proveedor, destino=ajuste_egreso, fecha_remito=datetime.now(), ajuste=True)
#                 r.save()
#                 re=Renglones(producto=producto, cantidad=int(sd1))
#                 re.save()
#                 re.nremito.add(r)
            
#             if int(sd1)< 0 and int(nc)>0: #ingresa insumo, funciona
#                 r=Remitos(tipo='I', origen=ajuste_ingreso, destino=umaad_centro, fecha_remito=datetime.now(), ajuste=True)
#                 r.save()
#                 re=Renglones(producto=producto, cantidad=int(nc)-int(sd1))
#                 re.save()
#                 re.nremito.add(r)

#             if int(sd1)>0 and int(nc)>0: #ingresa insumo porque recuento>stock 
#                 r=Remitos(tipo='I', origen=ajuste_ingreso, destino=umaad_centro, fecha_remito=datetime.now(), ajuste=True)
#                 r.save()
#                 re=Renglones(producto=producto, cantidad=-evaluador) #porque evaluador es negativo
#                 re.save()
#                 re.nremito.add(r)

#             if int(sd1)== 0: 
#                 r=Remitos(tipo='I', origen=ajuste_ingreso, destino=umaad_centro, fecha_remito=datetime.now(), ajuste=True)
#                 r.save()
#                 re=Renglones(producto=producto, cantidad=nc)
#                 re.save()
#                 re.nremito.add(r)
            
#         return render(request, 'inf/ciclico_stock.html', {"id":id, 'stock':stock, 'nc':nc, 'sd1':sd1 , 'evaluador':evaluador})

#     def calculo_stock(request): #tabla stocks_tabla
      
#         c=0
#         while c<3:
#             for i in range(1,500):
#                 try:
#                     q=Productos.objects.get(idproductos=i)
#                     q2=Stocks_tabla.objects.filter(producto=q).exists()
#                     if q2==True:
#                         pass
#                     else:
#                         Stocks_tabla.objects.create(producto=q)
#                         eg=Renglones.objects.create(producto=q, cantidad=0)
#                         eg.save()
#                         eg.nremito.add(1) #un remito de egreso
#                         ig=Renglones.objects.create(producto=q, cantidad=0)
#                         ig.save()
#                         ig.nremito.add(2) #un remito de ingreso
#                     c=c+1
#                 except:
#                     c=c+1
#                     continue
                
#         remitos_i=Remitos.objects.filter(destino=1)
#         renglones_i=Renglones.objects.filter(nremito__in=remitos_i)

#         remitos_e=Remitos.objects.filter(origen=1)
#         renglones_e=Renglones.objects.filter(nremito__in=remitos_e)

#         c=0
#         while c<2:
#             for i in range(1,500):
#                 try:
#                     ingreso=renglones_i.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
#                     egreso=renglones_e.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
#                     stock=sum(ingreso.values())-sum(egreso.values())
#                     Stocks_tabla.objects.filter(producto=i).update(stock_umaad=stock)
#                     c=c+1
#                 except TypeError:
#                     c=c+1
#                     continue
        
#         stock=Stocks_tabla.objects.all()
            
#         return render (request, 'inf/calculo_stock.html', {'stock':stock})
    
#     def stock_vd(request, id): #NCK
      
#         origen=Proveedor.objects.get(idproveedor=id)
#         destino=Centro.objects.get(idcentro=id)
        
#         c=0
#         while c<2: #el else busca que el bucle try no se anule por la aparicion de un none
#             for i in range(1,500):
#                 try:
#                     q=Productos.objects.get(idproductos=i)
#                     q2=Stocks_tabla.objects.filter(producto=q).exists()
#                     if q2==True:
#                         pass
#                     else:
#                         Stocks_tabla.objects.create(producto=q)
                        
#                         eg=Renglones.objects.create(producto=q, cantidad=0)
#                         eg.save()
#                         eg.nremito.add(9) #un remito de egreso
#                         ig=Renglones.objects.create(producto=q, cantidad=0)
#                         ig.save()
#                         ig.nremito.add(8) #un remito de ingreso
#                     c=c+1
#                 except:
#                     c=c+1
#                     continue
        
#         #update del campo stock_umaad
#         remitos_i=Remitos.objects.filter(destino=id)
#         renglones_i=Renglones.objects.filter(nremito__in=remitos_i)
#         remitos_e=Remitos.objects.filter(origen=id)
#         renglones_e=Renglones.objects.filter(nremito__in=remitos_e)

#         c=0
#         while c<2:
#             for i in range(1,500):
#                 try:
#                     ingreso=renglones_i.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
#                     egreso=renglones_e.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
#                     stock=sum(ingreso.values())-sum(egreso.values())
#                     Stocks_tabla.objects.filter(producto=i).update(stock_nck=stock)
#                     c=c+1
#                 except TypeError:
#                     c=c+1
#                     continue
        
#         stock=Stocks_tabla.objects.all()
        
#         return render (request, 'inf/stock_vd.html', {'stock':stock})

# class Consumo(HttpRequest):

#     def consumo_centro(request): #pagina para opciones
#         centro=Centro.objects.all()
#         centro_input=request.POST.get('centro')
#         if request.method=='POST':
#             centro_input=centro_input
#         centro_sel=Centro.objects.filter(idcentro=centro_input)
#         return render(request, 'inf/consumo_centro.html', {'centro':centro, 'centro_sel':centro_sel})
    
#     def consumo_centro_vd(request, id):# consumo total del centro, agregar costo
#         idc=Centro.objects.get(idcentro=id)
        
#         remitos=Remitos.objects.all().filter(destino=id)
#         renglones=Renglones.objects.filter(nremito__in=remitos) 
#         idcentro=Centro.objects.get(idcentro=id)
#         producto_en_renglones=Productos.objects.filter(idproductos__in=renglones)
        
#         c=0

#         while c<2: 
#             for i in range(1,500):
#                 try:
#                     q=Productos.objects.get(idproductos=i)
#                     q2=Totales.objects.filter(producto=q).filter(centro=idcentro).exists()
                    
#                     if q2 == True:#update
#                         egreso=Renglones.objects.filter(nremito__in=Remitos.objects.filter(destino=id)).filter(producto=q).aggregate(total=Sum('cantidad'))
#                         cant=sum(egreso.values())
#                         Totales.objects.filter(centro=idcentro).filter(producto=q).update(cantidad=cant)
#                         c=c+1 
#                     else: #create
#                         Totales.objects.create(centro=idcentro, producto=q, cantidad=0)
#                         c=c+1
#                 except:
#                     error='No anda'
#                     c=c+1
#                     continue

#         consumo=Totales.objects.filter(centro=id)#.exclude(cantidad=0)
        
#         return render(request, 'inf/consumo_centro_vd.html', {'idc':idc, 'consumo':consumo})

#     def consumo_unidad_total(request, id):
#         idc=Centro.objects.get(idcentro=id)
        
#         remitos=Remitos.objects.all().filter(destino=id)
#         renglones=Renglones.objects.filter(nremito__in=remitos) 
#         idcentro=Centro.objects.get(idcentro=id)
        
#         c=0

#         while c<2: 
#             for i in range(1,500):
#                 try:
#                     q=Productos.objects.get(idproductos=i)
#                     q2=Totales.objects.filter(producto=q).filter(centro=idcentro).exists()
                    
#                     if q2 == True:
#                         egreso=Renglones.objects.filter(nremito__in=Remitos.objects.filter(destino=id)).filter(producto=q).aggregate(total=Sum('cantidad'))
#                         cant=sum(egreso.values())
#                         costo=cant*(q.precio)
#                         Totales.objects.filter(centro=idcentro).filter(producto=q).update(cantidad=cant, costo=costo)
#                         c=c+1 
#                     else: 
#                         Totales.objects.create(centro=idcentro, producto=q, cantidad=0, costo=0)
#                         c=c+1
#                 except:
#                     error='No anda'
#                     c=c+1
#                     continue

#         consumo=Totales.objects.filter(centro=id).exclude(cantidad=0)
#         consumo_total=consumo.aggregate(Sum('costo'))
#         return render(request, 'inf/consumo_unidad_total.html', {'idc':idc, 'consumo':consumo, 'consumo_total':consumo_total})
    
#     def consumo_mensual_centro(request, id): #consumo x mes, guarda en clase consumo_mensuales
        
#         mes=request.POST.get('mes')
#         mes3=str(1)
#         mes4=str()
#         if request.method=='POST':
#             mes=mes
#             mes2=datetime.strptime(mes, '%Y-%m-%d')
#             mes3=mes2.strftime('%m')
#             mes4=mes2.strftime('%Y')

#         idc=Centro.objects.get(idcentro=id)     
#         remitos=Remitos.objects.all().filter(destino=id).filter(fecha_remito__month=mes3) #gobierna cambios
#         renglones=Renglones.objects.filter(nremito__in=remitos) 
        
#         q=QuerySet()
        
#         q=Productos.objects.all()
#         c=0

#         while c<2: 
#             for i in range(1,500):
#                 try:
#                     q=Productos.objects.get(idproductos=i)
#                     q2=Consumos_mensuales.objects.filter(producto=q).filter(centro=idc).filter(fecha=mes).exists()
                    
#                     if q2 == True:
#                         egreso=Renglones.objects.filter(nremito__in=remitos).filter(producto=q).aggregate(total=Sum('cantidad'))
#                         cant=sum(egreso.values())
#                         Consumos_mensuales.objects.filter(centro=idc).filter(producto=q).filter(fecha=mes).update(cantidad=cant)

#                         prod=Productos.objects.filter(idproductos=i).aggregate(Sum('precio'))
                        
#                         can=Consumos_mensuales.objects.filter(centro=idc).filter(producto=q).filter(fecha=mes).aggregate(Sum('cantidad'))
#                         prod2=sum(prod.values())
#                         can2=sum(can.values())
#                         costo2=prod2*can2

#                         Consumos_mensuales.objects.filter(centro=idc).filter(producto=q).filter(fecha=mes).update(costo=costo2)
                       
#                         c=c+1 
#                     else: #create
#                         Consumos_mensuales.objects.create(centro=idc, producto=q, cantidad=0, fecha=mes)
#                         c=c+1
#                 except:

#                     c=c+1 
#                     continue
        
#         costo_total=Consumos_mensuales.objects.filter(centro=id).filter(fecha=mes).aggregate(Sum('costo'))
#         consumo=Consumos_mensuales.objects.filter(centro=id).filter(fecha=mes).exclude(cantidad=0).order_by('producto')
        
        
#         return render (request, 'inf/consumo_mensual_centro.html', {'idc':idc, 'consumo':consumo, 'costo_total':costo_total, 'mes':mes3, 'mes4':mes4})

#     def consumo_historico_centro(request, id): #ojo que va en total, historico es una vista de querys

#         idc=Centro.objects.get(idcentro=id)
#         producto=Productos.objects.all()
#         remitos=Remitos.objects.filter(destino=id)
#         renglones=Renglones.objects.filter(nremito__in=remitos)
#         c=0
#         q=QuerySet()
#         prod2=int()
#         can2=int()
#         costo2=int()
#         while c<2:
#             for i in range(1,500):
#                 try:
#                     q=Productos.objects.get(idproductos=i)
#                     q2=Consumos_totales.objects.filter(producto=q).filter(centro=idc).exists()
                    
#                     if q2 == True:
#                         egreso=renglones.filter(producto=q).aggregate(total=Sum('cantidad'))
#                         cant=sum(egreso.values())
#                         Consumos_totales.objects.filter(centro=idc).filter(producto=q).update(cantidad=cant)
                        
#                         prod=Productos.objects.filter(idproductos=i).aggregate(Sum('precio'))
                        
#                         can=Consumos_totales.objects.filter(centro=idc).filter(producto=q).aggregate(Sum('cantidad'))
#                         prod2=sum(prod.values())
#                         can2=sum(can.values())
#                         costo2=prod2*can2

#                         Consumos_totales.objects.filter(centro=idc).filter(producto=q).update(costo=costo2)
#                         c=c+1 
#                     else: 
#                         Consumos_totales.objects.create(centro=idc, producto=q, cantidad=0)
#                         c=c+1
#                 except: 

#                     c=c+1 
#                     continue
    
#         consumo=Consumos_totales.objects.filter(centro=id).order_by('-cantidad').exclude(cantidad=0)
#         costo_total=Consumos_totales.objects.filter(centro=id).order_by('-costo').exclude(cantidad=0).aggregate(Sum('costo'))

#         return render (request, 'inf/consumo_historico_centro.html', {'idc':idc, 'remitos':remitos, 'consumo':consumo, 'costo_total':costo_total})
    
#     def evolucion_centro(request, id):
#         idc=Centro.objects.get(idcentro=id)

#         octubre=Consumos_mensuales.objects.filter(centro=id).filter(fecha='2021-10-31').exclude(cantidad=0)
#         costo_octubre=octubre.aggregate(Sum('costo'))

#         noviembre=Consumos_mensuales.objects.filter(fecha='2021-11-30').filter(centro=id).exclude(cantidad=0)
#         costo_noviembre=noviembre.aggregate(Sum('costo'))

#         diciembre=Consumos_mensuales.objects.filter(centro=id).filter(fecha='2021-12-31').exclude(cantidad=0)
#         costo_octubre=octubre.aggregate(Sum('costo'))

#         enero=Consumos_mensuales.objects.filter(fecha='2022-01-31').filter(centro=id).exclude(cantidad=0)
#         costo_noviembre=noviembre.aggregate(Sum('costo'))

#         return render(request, 'inf/evolucion_centro.html', {'idc':idc,'octubre':octubre, 'costo_octubre':costo_octubre, 'noviembre':noviembre, 'costo_novimebre':costo_noviembre})
    
#     def promedios(request, id): #umaad
#        #los datos de consumos mensuales deben estar actualizados
#        #los promedio son valores de cada centro.

#         c=0
#         while c<2:
#             for i in range(1,500):
#                 try:
#                     q=Productos.objects.get(idproductos=i)
#                     q2=Consumos_mensuales.objects.filter(producto=q).exists()
#                     if q2==True:
#                         promedio=Consumos_mensuales.objects.filter(centro=id).filter(producto=q).aggregate(Avg('cantidad'))
#                         promedio=sum(promedio.values())
#                         Consumos_mensuales.objects.filter(centro=id).filter(producto=q).update(promedio=promedio)
#                     else: #no debe crear objetos porque no filtra x mes y generara objetos innecesarios
#                         pass
#                     c=c+1
#                 except:
#                     c=c+1
#                     continue
        
#         promedio=Consumos_mensuales.objects.filter(centro=id).filter(fecha='2021-11-30')
#         return render(request, 'inf/medias.html', {'promedio':promedio})

#     def consumo_interno_nck_total(request): 
        
#         # remitos=Remitos.objects.filter(origen=2) #NCK es proveedor
#         # renglones=Renglones.objects.filter(nremito__in=remitos)


#         #el consumo interno del nck es simplemente el consumo de sus areas internas.
#         #ya sea porque lo proveyo el hospital o directamente la umaad.
#         #la vista deberia considerar el area para obtener informacion
        
#         return render(request, 'inf/consumo_interno_nck_total.html')
    


