from bibliosearch.controllers.dbController import insert_in_database, sql_connection
from bibliosearch.controllers.seleniumEngine import ARTICLE, BOOK, INPROCEEDINGS, Selenium
from django.shortcuts import  render
from django import forms
import json

def subir(request):
    if request.method == 'POST':
        formulario = FormularioSubir(request.POST)
        if formulario.is_valid():
            data = formulario.cleaned_data
            
            selenium = Selenium()
            tipos = []
            if data['articulo']:
                tipos.append(ARTICLE)
            if data['libro']:
                tipos.append(BOOK)
            if data['con_con']:
                tipos.append(INPROCEEDINGS)
            result = selenium.search(
                data['desde'], data['hasta'], '', tipos)

            with open('static/google_schoolar.json', 'w') as json_file:
                json.dump(result, json_file)
            json_file.close()

            path = 'static/google_schoolar.json'
            con = sql_connection() 
            insert_in_database(con, path)
            
            args = {
                'desde': data['desde'],
                'hasta':data['hasta'],
                'articulo':data['articulo'],
                'libro':data['libro'],
                'con_con':data['con_con']
            }
            return render(request, 'resultados_subida.html', args)
        
    else:
        formulario = FormularioSubir()


    return render(request, 'subir.html', {'formulario': formulario})


class FormularioSubir(forms.Form):
    articulo = forms.BooleanField(label='articulo',required=False)
    libro = forms.BooleanField(label='libro',required=False)
    con_con = forms.BooleanField(label='con_con',required=False)
    desde = forms.CharField(label='desde', max_length=4,min_length=4)
    hasta = forms.CharField(label='hasta',max_length=4,min_length=4)