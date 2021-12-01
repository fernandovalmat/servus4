from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
urlpatterns = [

    path('', views.estadisticas_home, name='home_info'),
    path('inf/consumo_total/', views.Stock.consumo_total, name='consumo_total'),
    #path('inf/stock/', views.Stock.stock, name='stock'),
    path('inf/ciclico_stock/<int:id>', views.Stock.ciclico_stock, name='ciclico_stock'),
    path('inf/consumo_centro/', views.Consumo.consumo_centro, name='consumo_centro'),
    path('inf/consumo_centro/<int:id>', views.Consumo.consumo_centro_vd, name='consumo_centro'),
    path('inf/consumo_unidad_total/<int:id>', views.Consumo.consumo_unidad_total),
    path('inf/consumo_mensual_centro/<int:id>', views.Consumo.consumo_mensual_centro),
    path('inf/consumo_historico_centro/<int:id>', views.Consumo.consumo_historico_centro),
    path('inf/calculo_stock/', views.Stock.calculo_stock),
    path('inf/evolucion_centro/<int:id>', views.Consumo.evolucion_centro),
    path('inf/medias/<int:id>', views.Consumo.promedios),
    path('inf/consumo_interno_nck_total/', views.Consumo.consumo_interno_nck_total, name='consumo_interno_nck_total'),
    path('inf/stock_vd/<int:id>', views.Stock.stock_vd, name='stock_vd'),
    path('inf/medias/<int:id>', views.Consumo.promedios, name='promedios'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)