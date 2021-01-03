from bibliosearch.controllers.dbController import insert_in_database, select_data, sql_connection
from bibliosearch.controllers.seleniumEngine import ARTICLE, BOOK, INPROCEEDINGS, Selenium
from django.shortcuts import  render
from django import forms


def buscar(request):
    if request.method == 'POST':
        formulario = FormularioBuscar(request.POST)
        if formulario.is_valid():
            data = formulario.cleaned_data
            
            tipos = []
            
            if data['articulo']:
                tipos.append('bbdd_articulo')
            if data['libro']:
                tipos.append('bbdd_libro')
            if data['con_con']:
                tipos.append('bbdd_com_con')

            titulo = data['titulo']
            autor = data['autor']
            desde = data['desde']
            hasta = data['hasta']

            selected_data = select_data(titulo, autor, desde, hasta, tipos)

            print(selected_data)
        
    else:
        formulario = FormularioBuscar()

    return render(request, 'buscar.html')

class FormularioBuscar(forms.Form):
    titulo = forms.CharField(label='titulo', required=False)
    autor = forms.CharField(label='autor', required=False)
    articulo = forms.BooleanField(label='articulo',required=False)
    con_con = forms.BooleanField(label='con_con',required=False)
    libro = forms.BooleanField(label='libro',required=False)
    desde = forms.CharField(label='desde', max_length=4,min_length=4)
    hasta = forms.CharField(label='hasta',max_length=4,min_length=4)
