from django import forms
from .models import *
from django.db.models import fields
from django.forms import ModelForm, widgets

class Remitos_form(forms.ModelForm):
    class Meta:
        model=Remitos
        fields='__all__'
        exclude=('costo',)

class Renglones_form(forms.Form):
    idrenglon=models.AutoField(primary_key=True)
    nremito=forms.ModelChoiceField(queryset=Remitos.objects.all().order_by('-idremito'))
    producto=forms.ModelChoiceField(queryset=Productos.objects.all().order_by('nombre_producto'))
    cantidad=forms.FloatField()