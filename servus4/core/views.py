from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
#from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def login(request):
    usuario=request.POST.get('usuario')
    password=request.POST.get('password')
    usuario_log=Login()

    if request.method=='POST':
        usuario=usuario
        password=password

    user = authenticate(request, username=usuario, password=password)
    if user is not None:
        #login (user)
        if usuario=='fvm':
            return redirect('/core/home_un/')
        else:
            return redirect('/core/home_ge/')
    # A backend authenticated the credentials
    else:
        pass
    # No backend authenticated the credentials
    return render(request, 'core/login.html', {'usuario_log':usuario_log, 'usuario':usuario})

@staff_member_required
def home_un(request):
    #debe traer el id de centro asociado al usuario
    #para esto, creaer un modelo que asocie usuarios con centros.
    return render(request, 'core/home_un.html')

@login_required
def home_ge(request):
    #debe traer el id de centro asociado al usuario
    #para esto, creaer un modelo que asocie usuarios con centros.
    usuario=request.POST.get('user')
        
    return render(request, 'core/home_ge.html', {'usuario':usuario})

    