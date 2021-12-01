from django import forms
from django.forms.fields import CharField



class Login(forms.Form):
    usuario=forms.CharField()
    password=forms.CharField()