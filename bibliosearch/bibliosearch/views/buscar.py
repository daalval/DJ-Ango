from bibliosearch.controllers.dbController import insert_in_database, select_data, sql_connection
from django.shortcuts import  render
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

            tipos = []

            if articulo:
                tipos.append('bbdd_articulo')
            if libro:
                tipos.append('bbdd_libro')
            if com_con:
                tipos.append('bbdd_com_con')

            page = 1

            full_list = select_data(titulo, autor, desde, hasta, tipos)

            print(full_list)

            max_page = math.ceil(len(full_list) / MAX_ITEMS)

            first_index = (page - 1) * MAX_ITEMS
            last_index = page * MAX_ITEMS

            list = full_list[first_index:last_index]

            rows = math.ceil(len(list) / MAX_ROWS)

            url_previus = f"/resultados/{titulo}/{autor}/{desde}/{hasta}/{articulo}/{libro}/{com_con}/{page - 1}/" if page > 1 else None
            url_next = f"/resultados/{titulo}/{autor}/{desde}/{hasta}/{articulo}/{libro}/{com_con}/{page + 1}/" if page < max_page else None

            args = {
                'list': list,
                'page': page,
                'max_page': max_page,
                'titulo': data['titulo'],
                'autor': data['autor'],
                'desde': data['desde'],
                'hasta':data['hasta'],
                'articulo':data['articulo'],
                'libro':data['libro'],
                'com_con':data['com_con'],
                'url_previus': url_previus,
                'url_next': url_next,
                'rows': rows
            }

            return render(request, 'resultados.html', args)
        
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
