from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include

urlpatterns = [

    path('', views.home_data, name='home_data'),

    path('data_app/agregar_centro/', views.Agregar_centro.agregar_centro, name='agregar_centro'),
    path('data_app/guardar_centro/', views.Agregar_centro.guardar_centro, name='guardar_centro'),
    path('data_app/editar_centro/', views.Agregar_centro.borrar_centro, name='editar_centro'),

    path('data_app/agregar_producto/', views.Productos_edit.agregar_producto, name='agregar_producto'),
    path('data_app/guardar_producto/', views.Productos_edit.guardar_producto, name='guardar_producto'),
    path('data_app/borrar_producto/', views.Productos_edit.borrar_producto, name='borrar_producto'),
    path('data_app/actualizar_precio/', views.Productos_edit.actualizar_precios, name='actualizar_precio'),
    path('data_app/lista_productos/', views.Productos_edit.lista_productos, name='lista productos'),
    path('data_app/agregar_proveedor/', views.Proveedores_edit.agregar_proveedor, name='proveedor'),
    path('data_app/guardar_proveedor/', views.Proveedores_edit.guardar_proveedor, name='guardar_proveedor'),
    path('data_app/borrar_proveedor/', views.Proveedores_edit.borrar_proveedor, name='borrar_proveedor'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)