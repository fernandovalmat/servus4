from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name="login"),
    path('home_un/', views.home_un, name="home_un"),
    path('home_ge/', views.home_ge, name="home_ge"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)