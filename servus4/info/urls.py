from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from .views import *
urlpatterns = [

    path('', views.estadisticas_home, name='home_info'),
    #path('info/consumo_total/', views.Stock.consumo_total, name='consumo_total'),
    
    
    path('info/consumo_total/', views.Stock.consumo_total, name='consumo_total'),
    
    

    
    path('info/ciclico_stock/<int:id>', views.Stock.ciclico_stock, name='ciclico_stock'),
    path('info/consumo_centro/', views.Consumo.consumo_centro, name='consumo_centro'),
    path('info/consumo_centro/<int:id>', views.Consumo.consumo_centro_vd, name='consumo_centro'),
    path('info/consumo_unidad_total/<int:id>', views.Consumo.consumo_unidad_total),
    path('info/consumo_mensual_centro/<int:id>', views.Consumo.consumo_mensual_centro),
    path('info/consumo_historico_centro/<int:id>', views.Consumo.consumo_historico_centro),
    path('info/calculo_stock/', views.Stock.calculo_stock),
    path('info/evolucion_centro/<int:id>', views.Consumo.evolucion_centro),
    path('info/medias/<int:id>', views.Consumo.promedios),
    path('info/consumo_interno_nck_total/', views.Consumo.consumo_interno_nck_total, name='consumo_interno_nck_total'),
    path('info/consumo_interno_nck_total/<int:id>', views.Consumo.consumo_interno_nck_total, name='consumo_interno_nck_total'),

   path('info/stock_vd/<int:id>', views.Stock.stock_vd, name='stock_vd'),
    path('info/medias/<int:id>', views.Consumo.promedios, name='promedios'),
    path('info/resumen_centros/', views.Consumo.resumen_centros, name='resumen centros'),
    path('info/resumen_productos/', views.Consumo.resumen_productos, name='resumen centros'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)