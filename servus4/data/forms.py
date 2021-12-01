from data.models import Centro, Productos, Proveedor
from django import forms
from django.db.models import fields
from django.forms import ModelForm

class Centro_form(forms.ModelForm):
    class Meta:
        model=Centro
        fields='__all__'

class Productos_form(forms.ModelForm):
    class Meta:
        model=Productos
        fields='__all__'

class Proveedores_form(forms.ModelForm):
    class Meta:
        model=Proveedor
        fields='__all__'