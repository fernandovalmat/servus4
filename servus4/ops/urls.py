from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include

urlpatterns = [

    path('', views.home_ops, name='home_ops'),
    path('ops/operaciones/', views.Operaciones.crear_remito, name='operaciones'),
    path('ops/edicion_dinamica/<int:id>', views.Operaciones.edicion_dinamica, name='edicion_dinamica'),
    path('ops/vd_remito_terminado/<int:id>', views.Operaciones.vd_remito_terminado, name='vd_remito_terminado'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
