from bibliosearch.controllers.dbController import insert_in_database, select_data, sql_connection
from django.shortcuts import  redirect, render
from django import forms
import math

MAX_ITEMS = 9
MAX_ROWS = 3


def buscar(request):
    if request.method == 'POST':
        formulario = FormularioBuscar(request.POST)
        if formulario.is_valid():
            data = formulario.cleaned_data

            titulo = data['titulo']
            autor = data['autor']
            desde = data['desde']
            hasta = data['hasta']

            articulo = data['articulo']
            libro = data['libro']
            com_con = data['com_con']


            return redirect(f'/resultados/{titulo}/{autor}/{desde}/{hasta}/{articulo}/{libro}/{com_con}/1')
        
    else:
        formulario = FormularioBuscar()

    return render(request, 'buscar.html')

    

class FormularioBuscar(forms.Form):
    titulo = forms.CharField(label='titulo', required=False)
    autor = forms.CharField(label='autor', required=False)
    articulo = forms.BooleanField(label='articulo',required=False)
    com_con = forms.BooleanField(label='com_con',required=False)
    libro = forms.BooleanField(label='libro',required=False)
    desde = forms.CharField(label='desde', max_length=4,min_length=4)
    hasta = forms.CharField(label='hasta',max_length=4,min_length=4)
