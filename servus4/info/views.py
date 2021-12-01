from django.shortcuts import render

from datetime import datetime
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.shortcuts import render
from django.db.models import Sum, Avg
from data.models import *
from ops.models import *
from .models import Consumos_mensual_1, Consumos_mensuales2, Consumos_totales2, Totales2, Stocks_tabla2, Ies

from django.utils import timezone





#IMPORTANTE
#CREAR FUNCIONES DE ACTUALIZACION DE TODAS LAS TABLAS.
#VER SI SE PUEDE HACER ALGO QUE ACTUALICE CUANDO ESTA EN ONLINE A DETERMINADA HORA.

def estadisticas_home(request):
    return render (request, 'home.html')
class Stock(HttpRequest):
    #umaad y nck requieren su propia funcion de calculo de mensuales combinada con promedio
    #Puede haber una forma de hacer todo junto con bucles

    def consumo_total(request): #de la umaad, OK, lista
        #hacer funcion analoga de nck
        
        
        #MENSUALES
        centro=Proveedor.objects.get(nombre_proveedor='umaad')
        remitos=Remitos.objects.filter(origen=centro).exclude(ajuste=True)
        renglones=Renglones.objects.filter(nremito__in=remitos)
        
        años=(2021, 2022)
        meses=(1,2,3,4,5,6,7,8,9,10,11,12)
        c=0
        while c<2:
            for a in años:
                for m in meses:
                    for i in range(1,500):
                        try:
                            q=Productos.objects.get(idproductos=i)
                            q2=Consumos_mensual_1.objects.filter(anio=a).filter(mes=m).filter(centro=centro).filter(producto=q).exists()
                            if q2==True: #existe
                                
                                rem=remitos.filter(fecha_remito__year=a).filter(fecha_remito__month=m)
                                
                                cantidad=renglones.filter(nremito__in=rem).filter(producto=q).aggregate(Sum('cantidad'))
                                cant=sum(cantidad.values())
                                
                                producto=Productos.objects.filter(idproductos=i).aggregate(Sum('precio'))
                                prod=sum(producto.values())
                                
                                costo=prod*cant
                                Consumos_mensual_1.objects.filter(centro=centro).filter(anio=a).filter(mes=m).filter(producto=q).update(cantidad=cant, costo=costo)
                                
                                c=c+1
                            else: 
                                Consumos_mensual_1.objects.create(centro=centro, anio=a, mes=m, producto=q, cantidad=0)
                                c=c+1
                                pass

                        except:
    
                            c=c+1
                            continue

        
        umad=Centro.objects.get(nombre_centro='umaad')
        umaad=Proveedor.objects.get(nombre_proveedor='umaad')

        #INGRESOS
        c=0
        while c<5:
            for idproducto in range(1,500):
                try:
                    suma_ingreso_producto=Renglones.objects.filter(nremito__in=Remitos.objects.filter(destino=umad).exclude(ajuste=True)).filter(producto=idproducto).aggregate(total_eg=Sum('cantidad'))
                    ingreso_t=sum(suma_ingreso_producto.values())
                    
                    Stocks_tabla2.objects.filter(producto=idproducto).update(ingreso_umaad=ingreso_t)
                except TypeError:
                    
                    Stocks_tabla2.objects.filter(producto=idproducto).update(ingreso_umaad=0)
                    c=c+1
                    continue
        #EGRESOS
        c=0
        while c<5:
            for idproducto in range(1,500):
                try:
                    suma_egreso_producto=Renglones.objects.filter(nremito__in=Remitos.objects.filter(origen=umaad).exclude(ajuste=True)).filter(producto=idproducto).aggregate(total_eg=Sum('cantidad'))
                    egreso_t=sum(suma_egreso_producto.values())
                 
                    Stocks_tabla2.objects.filter(producto=idproducto).update(egreso_umaad=egreso_t)
                except TypeError:
                    
                    Stocks_tabla2.objects.filter(producto=idproducto).update(egreso_umaad=0)
                    c=c+1
                    continue
        #STOCK
        c=0
        while c<3:
            for i in range(1,500):
                try:
                    q=Productos.objects.get(idproductos=i)
                    q2=Stocks_tabla2.objects.filter(producto=q).exists()
                    if q2==True:
                        pass
                    else:
                        Stocks_tabla2.objects.create(producto=q)
                        eg=Renglones.objects.create(producto=q, cantidad=0)
                        eg.save()
                        eg.nremito.add(1) #un remito de egreso
                        ig=Renglones.objects.create(producto=q, cantidad=0)
                        ig.save()
                        ig.nremito.add(2) #un remito de ingreso
                    c=c+1
                except:
                    c=c+1
                    continue
                
        remitos_i=Remitos.objects.filter(destino=1)
        renglones_i=Renglones.objects.filter(nremito__in=remitos_i)

        remitos_e=Remitos.objects.filter(origen=1)
        renglones_e=Renglones.objects.filter(nremito__in=remitos_e)

        c=0
        while c<2:
            for i in range(1,500):
                try:
                    ingreso=renglones_i.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
                    egreso=renglones_e.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
                    stock=sum(ingreso.values())-sum(egreso.values())
                    Stocks_tabla2.objects.filter(producto=i).update(stock_umaad=stock)
                    c=c+1
                except TypeError:
                    c=c+1
                    continue
        
        #PROMEDIO
        idc=Proveedor.objects.get(idproveedor=1)
        c=0
        while c<2:
            for i in range(1,500):
                try:
                    q=Productos.objects.get(idproductos=i)
                    q2=Consumos_mensual_1.objects.filter(producto=q).exists()
                    if q2==True:
                        promedio=Consumos_mensual_1.objects.filter(centro=idc).filter(producto=q).exclude(cantidad=0).aggregate(Avg('cantidad'))
                        promedio=sum(promedio.values())

                        Stocks_tabla2.objects.filter(producto=q).update(promedio_umaad=promedio)
                        
                        precio=Productos.objects.filter(nombre_producto=q).aggregate(Sum('precio'))
                        costo_prom=sum(promedio.values())*sum(precio.values())
                        Consumos_mensual_1.objects.filter(centro=idc).filter(producto=q).update(costopromedio=costo_prom)

                    else: #no debe crear objetos porque no filtra x mes y generara objetos innecesarios
                        pass
                    c=c+1
                except:
                    c=c+1
                    continue
        
        #DURACION
        #DURACION COMBINA DOS VALORES: STOCK Y PROMEDIO, QUE SE ACTUALIZAN EN ESTA MISMA FUNCION
        #SE ASIGNANDO AL CAMPO DURACION_UMAAD ITERANDO PRODUCTOS
        #ES PARECIDA A LA VISTA DE PROMEDIOS

        c=0
        while c<2:
            for i in range(1,500):
                try:
                    q=Productos.objects.get(idproductos=i)
                    q2=Stocks_tabla2.objects.filter(producto=q).exists()
                    if q2==True:
                        prom=Stocks_tabla2.objects.filter(producto=q).aggregate(Sum('promedio_umaad'))
                        sto=Stocks_tabla2.objects.filter(producto=q).aggregate(Sum('stock_umaad'))
                        duracion=sum(sto.values())/sum(prom.values())
                        Stocks_tabla2.objects.filter(producto=q).update(duracion_umaad=duracion)
                        c=c+1
                    else:
                        pass
                except:
                   
                    c=c+1
                    continue

        consumo=Stocks_tabla2.objects.all().order_by('producto')        
        return render (request, 'info/consumo_total.html', {'consumo':consumo})
    
    
    

    def ciclico_stock(request, id): 
       
        stock=Stocks_tabla2.objects.filter(producto=id)
       
        sd1=request.POST.get('sd1')
        nc=request.POST.get('nc')
        evaluador=0
        ajuste_ingreso=Proveedor.objects.get(nombre_proveedor='ajustes') #umaad: 6
        ajuste_egreso=Centro.objects.get(nombre_centro='ajustes') #umaad:9

        umaad_proveedor=Proveedor.objects.get(nombre_proveedor='UMAAD')
        umaad_centro=Centro.objects.get(nombre_centro='UMAAD') #umaad:9
        
        producto=Productos.objects.get(idproductos=id)
        if request.method=='POST': 
            
            evaluador=int(sd1)-int(nc) #stock - recuento

            if int(sd1)<0 and int(nc)==0: #ingresa insumo DESDE AJUSTE INGRESO QUE ES EL PROVEEDOR
                r=Remitos(tipo='I', origen=ajuste_ingreso, destino=umaad_centro, fecha_remito=datetime.now(), ajuste=True)
                r.save()
                re=Renglones(producto=producto, cantidad=-int(sd1))
                re.save()
                re.nremito.add(r)
            
            if int(sd1)> 0 and int(nc)==0: #egresa insumo , FUNCIONA
                r=Remitos(tipo='E', origen=umaad_proveedor, destino=ajuste_egreso, fecha_remito=datetime.now(), ajuste=True)
                r.save()
                re=Renglones(producto=producto, cantidad=int(sd1))
                re.save()
                re.nremito.add(r)
            
            if int(sd1)< 0 and int(nc)>0: #ingresa insumo, funciona
                r=Remitos(tipo='I', origen=ajuste_ingreso, destino=umaad_centro, fecha_remito=datetime.now(), ajuste=True)
                r.save()
                re=Renglones(producto=producto, cantidad=int(nc)-int(sd1))
                re.save()
                re.nremito.add(r)

            if int(sd1)>0 and int(nc)>0: #ingresa insumo porque recuento>stock 
                r=Remitos(tipo='I', origen=ajuste_ingreso, destino=umaad_centro, fecha_remito=datetime.now(), ajuste=True)
                r.save()
                re=Renglones(producto=producto, cantidad=-evaluador) #porque evaluador es negativo
                re.save()
                re.nremito.add(r)

            if int(sd1)== 0: 
                r=Remitos(tipo='I', origen=ajuste_ingreso, destino=umaad_centro, fecha_remito=datetime.now(), ajuste=True)
                r.save()
                re=Renglones(producto=producto, cantidad=nc)
                re.save()
                re.nremito.add(r)
            
        return render(request, 'info/ciclico_stock.html', {"id":id, 'stock':stock, 'nc':nc, 'sd1':sd1 , 'evaluador':evaluador})

    def calculo_stock(request): 
      
        c=0
        while c<3:
            for i in range(1,500):
                try:
                    q=Productos.objects.get(idproductos=i)
                    q2=Stocks_tabla2.objects.filter(producto=q).exists()
                    if q2==True:
                        pass
                    else:
                        Stocks_tabla2.objects.create(producto=q)
                        eg=Renglones.objects.create(producto=q, cantidad=0)
                        eg.save()
                        eg.nremito.add(1) #un remito de egreso
                        ig=Renglones.objects.create(producto=q, cantidad=0)
                        ig.save()
                        ig.nremito.add(2) #un remito de ingreso
                    c=c+1
                except:
                    c=c+1
                    continue
                
        remitos_i=Remitos.objects.filter(destino=1)
        renglones_i=Renglones.objects.filter(nremito__in=remitos_i)

        remitos_e=Remitos.objects.filter(origen=1)
        renglones_e=Renglones.objects.filter(nremito__in=remitos_e)

        c=0
        while c<2:
            for i in range(1,500):
                try:
                    ingreso=renglones_i.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
                    egreso=renglones_e.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
                    stock=sum(ingreso.values())-sum(egreso.values())
                    Stocks_tabla2.objects.filter(producto=i).update(stock_umaad=stock)
                    c=c+1
                except TypeError:
                    c=c+1
                    continue
        
        
        stock=Stocks_tabla2.objects.all()
        
        return render (request, 'info/calculo_stock.html', {'stock':stock})
        
    def stock_vd(request, id): #NCK
        
       
        origen=Proveedor.objects.get(idproveedor=id)
        destino=Centro.objects.get(idcentro=id)
        
        c=0
        while c<2: #el else busca que el bucle try no se anule por la aparicion de un none
            for i in range(1,500):
                try:
                    q=Productos.objects.get(idproductos=i)
                    q2=Stocks_tabla2.objects.filter(producto=q).exists() #ies
                    if q2==True:
                        pass
                    else:
                        Stocks_tabla2.objects.create(producto=q)
                        
                        eg=Renglones.objects.create(producto=q, cantidad=0)
                        eg.save()
                        eg.nremito.add(9) #un remito de egreso
                        ig=Renglones.objects.create(producto=q, cantidad=0)
                        ig.save()
                        ig.nremito.add(8) #un remito de ingreso
                    c=c+1
                except:
                    c=c+1
                    continue
        
        #update del campo stock_nck
        remitos_i=Remitos.objects.filter(destino=id)
        renglones_i=Renglones.objects.filter(nremito__in=remitos_i)
        remitos_e=Remitos.objects.filter(origen=id)
        renglones_e=Renglones.objects.filter(nremito__in=remitos_e)

        c=0
        while c<2:
            for i in range(1,500):
                try:
                    ingreso=renglones_i.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
                    egreso=renglones_e.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
                    stock=sum(ingreso.values())-sum(egreso.values())
                    Stocks_tabla2.objects.filter(producto=i).update(stock_nck=stock)
                    c=c+1
                except TypeError:
                    c=c+1
                    continue
        
        stock=Stocks_tabla2.objects.all()
        
        return render (request, 'info/stock_vd.html', {'stock':stock})

class Consumo(HttpRequest):

    def consumo_centro(request): #pagina para opciones
        centro=Centro.objects.all().exclude(nombre_centro='UMAAD')
        #esto se setea despues del deploy
        #hospitales
        
        #udps

        #CAPS

        #otros

        centro_input=request.POST.get('centro')
        if request.method=='POST':
            centro_input=centro_input
        centro_sel=Centro.objects.filter(idcentro=centro_input)
        return render(request, 'info/consumo_centro.html', {'centro':centro, 'centro_sel':centro_sel})
    
    def consumo_centro_vd(request, id):# consumo total del centro, agregar costo
        idc=Centro.objects.get(idcentro=id)
        
        remitos=Remitos.objects.all().filter(destino=id)
        renglones=Renglones.objects.filter(nremito__in=remitos) 
        idcentro=Centro.objects.get(idcentro=id)
        producto_en_renglones=Productos.objects.filter(idproductos__in=renglones)
        
        c=0

        while c<2: 
            for i in range(1,500):
                try:
                    q=Productos.objects.get(idproductos=i)
                    q2=Totales2.objects.filter(producto=q).filter(centro=idcentro).exists()
                    
                    if q2 == True:#update
                        egreso=Renglones.objects.filter(nremito__in=Remitos.objects.filter(destino=id)).filter(producto=q).aggregate(total=Sum('cantidad'))
                        cant=sum(egreso.values())
                        Totales2.objects.filter(centro=idcentro).filter(producto=q).update(cantidad=cant)
                        c=c+1 
                    else: #create
                        Totales2.objects.create(centro=idcentro, producto=q, cantidad=0)
                        c=c+1
                except:
                    error='No anda'
                    c=c+1
                    continue

        consumo=Totales2.objects.filter(centro=id)#.exclude(cantidad=0)
        
        return render(request, 'info/consumo_centro_vd.html', {'idc':idc, 'consumo':consumo})

    def consumo_unidad_total(request, id):
        idc=Centro.objects.get(idcentro=id)
        
        remitos=Remitos.objects.all().filter(destino=id)
        renglones=Renglones.objects.filter(nremito__in=remitos) 
        idcentro=Centro.objects.get(idcentro=id)
        
        c=0

        while c<2: 
            for i in range(1,500):
                try:
                    q=Productos.objects.get(idproductos=i)
                    q2=Totales2.objects.filter(producto=q).filter(centro=idcentro).exists()
                    
                    if q2 == True:
                        egreso=Renglones.objects.filter(nremito__in=Remitos.objects.filter(destino=id)).filter(producto=q).aggregate(total=Sum('cantidad'))
                        cant=sum(egreso.values())
                        costo=cant*(q.precio)
                        Totales2.objects.filter(centro=idcentro).filter(producto=q).update(cantidad=cant, costo=costo)
                        c=c+1 
                    else: 
                        Totales2.objects.create(centro=idcentro, producto=q, cantidad=0, costo=0)
                        c=c+1
                except:
                    error='No anda'
                    c=c+1
                    continue

        consumo=Totales2.objects.filter(centro=id).exclude(cantidad=0).order_by('producto')
        consumo_total=consumo.aggregate(Sum('costo'))
        return render(request, 'info/consumo_unidad_total.html', {'idc':idc, 'consumo':consumo, 'consumo_total':consumo_total})
    
    def consumo_mensual_centro(request, id): 
       
        centro=Centro.objects.get(idcentro=id)
        remitos=Remitos.objects.filter(destino=centro)
        renglones=Renglones.objects.filter(nremito__in=remitos)
        
        años=(2021, 2022)
        meses=(1,2,3,4,5,6,7,8,9,10,11,12)
     
        c=0
        while c<2:
            for a in años:
                for m in meses:
                    for i in range(1,500):
                        try:
                            q=Productos.objects.get(idproductos=i)
                            q2=Consumos_mensuales2.objects.filter(centro=centro).filter(anio=a).filter(mes=m).filter(producto=q).exists()
                            if q2==True: #existe
                                
                                rem=remitos.filter(fecha_remito__year=a).filter(fecha_remito__month=m)
                                
                                cantidad=renglones.filter(nremito__in=rem).filter(producto=q).aggregate(Sum('cantidad'))
                                cant=sum(cantidad.values())
                                
                                producto=Productos.objects.filter(idproductos=i).aggregate(Sum('precio'))
                                prod=sum(producto.values())
                                
                                costo=prod*cant
                                Consumos_mensuales2.objects.filter(centro=centro).filter(anio=a).filter(mes=m).filter(producto=q).update(cantidad=cant, costo=costo)
                                
                                c=c+1
                            else: 
                                Consumos_mensuales2.objects.create(centro=centro, anio=a, mes=m, producto=q, cantidad=0)
                                c=c+1
                                pass

                        except:
    
                            c=c+1
                            continue
        
        #este forma a otra pagina con vd, asi no impacta tanto en la consulta
        mes=request.POST.get('mes')
        anio=request.POST.get('anio')
        if request.method=='POST':
            mes=mes
            anio=anio
        consumo=Consumos_mensuales2.objects.filter(centro=id).filter(anio=anio).filter(mes=mes)
        costo=consumo.aggregate(Sum('costo'))
        
        return render(request, 'info/consumo_mensual_centro.html', {'centro':centro, 'consumo':consumo, 'costo':costo, 'mes':mes, 'anio':anio}) 

    def consumo_historico_centro(request, id): #ojo que va en total, historico es una vista de querys

        idc=Centro.objects.get(idcentro=id)
        
        #para ver un producto
        producto=request.POST.get('producto')
        if request.method=='POST':
            producto=producto
        consumo=Consumos_mensuales2.objects.filter(centro=id).exclude(cantidad=0).order_by('producto')
           
        #usar annotate concatenado para que devuelva año - mes - cantidad
        #usar form de html para pasar producto
        #boton para activa todo?

        return render (request, 'info/consumo_historico_centro.html', {'idc':idc, 'consumo':consumo})
    
    def evolucion_centro(request, id):
        idc=Centro.objects.get(idcentro=id)

        octubre=Consumos_mensuales2.objects.filter(centro=idc).filter(anio=2021).filter(mes=10).exclude(cantidad=0)
        costo_octubre=octubre.aggregate(Sum('costo'))

        noviembre=Consumos_mensuales2.objects.filter(centro=idc).filter(anio=2021).filter(mes=11).exclude(cantidad=0)
        costo_noviembre=noviembre.aggregate(Sum('costo'))

        # diciembre=Consumos_mensuales2.objects.filter(centro=id).filter(fecha='2021-12-31').exclude(cantidad=0)
        # costo_octubre=octubre.aggregate(Sum('costo'))

        # enero=Consumos_mensuales2.objects.filter(fecha='2022-01-31').filter(centro=id).exclude(cantidad=0)
        # costo_noviembre=noviembre.aggregate(Sum('costo'))

        return render(request, 'info/evolucion_centro.html', {'idc':idc,'octubre':octubre, 'costo_octubre':costo_octubre, 'noviembre':noviembre, 'costo_novimebre':costo_noviembre})
    
    def promedios(request, id): #umaad
       #los datos de consumos mensuales deben estar actualizados
       #los promedio son valores de cada centro.
        idc=Centro.objects.get(idcentro=id)
        c=0
        while c<2:
            for i in range(1,500):
                try:
                    q=Productos.objects.get(idproductos=i)
                    q2=Consumos_mensuales2.objects.filter(producto=q).exists()
                    if q2==True:
                        promedio=Consumos_mensuales2.objects.filter(centro=id).filter(producto=q).exclude(cantidad=0).aggregate(Avg('cantidad'))
                        prom=sum(promedio.values())

                        Consumos_mensuales2.objects.filter(centro=id).filter(producto=q).update(promedio=prom)

                        precio=Productos.objects.filter(nombre_producto=q).aggregate(Sum('precio'))
                        costo_prom=sum(promedio.values())*sum(precio.values())
                        Consumos_mensuales2.objects.filter(centro=id).filter(producto=q).update(costopromedio=costo_prom)

                    else: #no debe crear objetos porque no filtra x mes y generara objetos innecesarios
                        pass
                    c=c+1
                except:
                    
                    c=c+1
                    continue
        
        promedio=Consumos_mensuales2.objects.filter(centro=id).filter(anio=2021).filter(mes=11)
        return render(request, 'info/medias.html', {'promedio':promedio, 'idc':idc})

    def consumo_interno_nck_total(request): #ok, lista, muestra nck proveedor
              
        nckp=Proveedor.objects.get(nombre_proveedor='HMNCK')

        centro=Centro.objects.get(nombre_centro='HMNCK')

        remitos=Remitos.objects.filter(destino=centro).exclude(ajuste=True)
        renglones=Renglones.objects.filter(nremito__in=remitos)
        
        #mensuales
        #es lo que ingresa al nck
        años=(2021, 2022)
        meses=(1,2,3,4,5,6,7,8,9,10,11,12)
        c=0
        while c<2:
            for a in años:
                for m in meses:
                    for i in range(1,500):
                        try:
                            q=Productos.objects.get(idproductos=i)
                            q2=Consumos_mensual_1.objects.filter(anio=a).filter(mes=m).filter(producto=q).filter(centro=nckp).exists()
                            if q2==True: #existe
                                
                                rem=remitos.filter(fecha_remito__year=a).filter(fecha_remito__month=m)
                                
                                cantidad=renglones.filter(nremito__in=rem).filter(producto=q).aggregate(Sum('cantidad'))
                                cant=sum(cantidad.values())
                                
                                producto=Productos.objects.filter(idproductos=i).aggregate(Sum('precio'))
                                prod=sum(producto.values())
                                
                                costo=prod*cant
                                Consumos_mensual_1.objects.filter(centro=nckp).filter(anio=a).filter(mes=m).filter(producto=q).update(cantidad=cant, costo=costo)
                                
                                c=c+1
                            else: 
                                Consumos_mensual_1.objects.create(centro=nckp, anio=a, mes=m, producto=q, cantidad=0)
                                c=c+1
                                pass

                        except:
    
                            c=c+1
                            continue

        #INGRESOS
        c=0
        while c<5:
            for idproducto in range(1,500):
                try:
                    suma_ingreso_producto=Renglones.objects.filter(nremito__in=Remitos.objects.filter(destino=centro).exclude(ajuste=True)).filter(producto=idproducto).aggregate(total_eg=Sum('cantidad'))
                    ingreso_t=sum(suma_ingreso_producto.values())
                    
                    Stocks_tabla2.objects.filter(producto=idproducto).update(ingreso_nck=ingreso_t)
                except TypeError:
                    
                    Stocks_tabla2.objects.filter(producto=idproducto).update(ingreso_nck=0)
                    c=c+1
                    continue
        #EGRESOS
        c=0
        while c<5:
            for idproducto in range(1,500):
                try:
                    suma_egreso_producto=Renglones.objects.filter(nremito__in=Remitos.objects.filter(origen=nckp).exclude(ajuste=True)).filter(producto=idproducto).aggregate(total_eg=Sum('cantidad'))
                    egreso_t=sum(suma_egreso_producto.values())
                 
                    Stocks_tabla2.objects.filter(producto=idproducto).update(egreso_nck=egreso_t)
                except TypeError:
                    
                    Stocks_tabla2.objects.filter(producto=idproducto).update(egreso_nck=0)
                    c=c+1
                    continue
        #STOCK
        c=0
        while c<3:
            for i in range(1,500):
                try:
                    q=Productos.objects.get(idproductos=i)
                    q2=Stocks_tabla2.objects.filter(producto=q).exists()
                    if q2==True:
                        pass
                    else:
                        Stocks_tabla2.objects.create(producto=q)
                        eg=Renglones.objects.create(producto=q, cantidad=0)
                        eg.save()
                        eg.nremito.add(54) #un remito de egreso
                        ig=Renglones.objects.create(producto=q, cantidad=0)
                        ig.save()
                        ig.nremito.add(55) #un remito de ingreso
                    c=c+1
                except:
                    c=c+1
                    continue
                
        remitos_i=Remitos.objects.filter(destino=centro)
        renglones_i=Renglones.objects.filter(nremito__in=remitos_i)

        remitos_e=Remitos.objects.filter(origen=nckp)
        renglones_e=Renglones.objects.filter(nremito__in=remitos_e)

        c=0
        while c<2:
            for i in range(1,500):
                try:
                    ingreso=renglones_i.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
                    egreso=renglones_e.filter(producto=i).aggregate(total_eg=Sum('cantidad'))
                    stock=sum(ingreso.values())-sum(egreso.values())
                    Stocks_tabla2.objects.filter(producto=i).update(stock_nck=stock)
                    c=c+1
                except TypeError:
                    c=c+1
                    continue
        
        #PROMEDIO (de egreso desde el nck)
        
        c=0
        while c<2:
            for i in range(1,500):
                try:
                    q=Productos.objects.get(idproductos=i)
                    q2=Consumos_mensual_1.objects.filter(producto=q).exists()
                    if q2==True:
                        promedio=Consumos_mensual_1.objects.filter(centro=nckp).filter(producto=q).exclude(cantidad=0).aggregate(Avg('cantidad'))
                        promedio=sum(promedio.values())

                        Stocks_tabla2.objects.filter(producto=q).update(promedio_nck=promedio)

                    else: #no debe crear objetos porque no filtra x mes y generara objetos innecesarios
                        pass
                    c=c+1
                except:
                    c=c+1
                    continue
        
        #DURACION
        #DURACION COMBINA DOS VALORES: STOCK Y PROMEDIO, QUE SE ACTUALIZAN EN ESTA MISMA FUNCION
        #SE ASIGNANDO AL CAMPO DURACION_UMAAD ITERANDO PRODUCTOS
        #ES PARECIDA A LA VISTA DE PROMEDIOS

        c=0
        while c<2:
            for i in range(1,500):
                try:
                    q=Productos.objects.get(idproductos=i)
                    q2=Stocks_tabla2.objects.filter(producto=q).exists()
                    if q2==True:
                        prom=Stocks_tabla2.objects.filter(producto=q).aggregate(Sum('promedio_nck'))
                        sto=Stocks_tabla2.objects.filter(producto=q).aggregate(Sum('stock_nck'))
                        duracion=sum(sto.values())/sum(prom.values())
                        Stocks_tabla2.objects.filter(producto=q).update(duracion_nck=duracion)
                        c=c+1
                    else:
                        pass
                except:
                   
                    c=c+1
                    continue

        consumo=Stocks_tabla2.objects.all().order_by('producto')  

        subareas=Centro.objects.filter(nombre_centro='NCK')
        return render(request, 'info/consumo_interno_nck_total.html', {'subareas':subareas, 'consumo':consumo})
    
    def resumen_centros(request):
        centros=Centro.objects.all()
        #tiene que traer los datos de consumos_mensuales_2
        #Query con opciones en html que pasan el id del centro
        idc=request.POST.get('idc')
        if request.method=='POST':
            idc=idc
        
        #costo total acumulado
        costo_total_acumulado=Consumos_mensuales2.objects.filter(centro=idc).exclude(cantidad=0).aggregate(total=Sum('costo'))
        #costo promedio mensual
        costo_promedio=Consumos_mensuales2.objects.filter(centro=idc).aggregate(total=Sum('costopromedio'))
        #costos mensuales
        octubre=Consumos_mensuales2.objects.filter(centro=idc).filter(anio=2021).filter(mes=10).exclude(cantidad=0)
        costo_octubre=octubre.aggregate(total=Sum('costo'))

        noviembre=Consumos_mensuales2.objects.filter(centro=idc).filter(anio=2021).filter(mes=11).exclude(cantidad=0)
        costo_noviembre=noviembre.aggregate(total=Sum('costo'))
        
        diciembre=Consumos_mensuales2.objects.filter(centro=idc).filter(anio=2021).filter(mes=12).exclude(cantidad=0)
        costo_noviembre=noviembre.aggregate(total=Sum('costo'))
        


        #productos mas usados
        producto_costo=Totales2.objects.filter(centro=idc).order_by('costo')[:20]
        pcp=Consumos_mensuales2.objects.filter(centro=idc).filter(mes=11).filter(anio=2021).order_by('costopromedio')[:20]


        return render(request, 'info/resumen_centros.html', {'centros':centros, 'costo_total_acumulado':costo_total_acumulado, 'costo_promedio':costo_promedio, 'octubre':costo_octubre, 'noviembre':costo_noviembre, 'producto_costo':producto_costo, 'pcp':pcp})

    def resumen_productos(request): 
        #con la tabla de datos de la umaad
        #segun egreso umaad
        umaad=Proveedor.objects.get(nombre_proveedor='UMAAD')
        egreso=Stocks_tabla2.objects.all().order_by('-egreso_umaad')

        costo=Consumos_mensual_1.objects.filter(centro=umaad).filter(anio=2021).filter(mes=12).order_by('costopromedio')
        

        return render(request, 'info/resumen_productos.html', {'egreso':egreso, 'costo':costo})
    