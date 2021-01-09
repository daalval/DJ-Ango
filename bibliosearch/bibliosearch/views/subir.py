from bibliosearch.controllers.seleniumEngine import Selenium
from bibliosearch.models.Com_con import COM_CON
from bibliosearch.models.Libro import LIBRO
from bibliosearch.models.Articulo import ARTICULO
from bibliosearch.controllers.ieeeEngine import query
from bibliosearch.controllers.xml2json import xml_parser
from bibliosearch.controllers.dbController import PATHS, insert_in_database, sql_connection
from django.shortcuts import  render
from django import forms
import json

def subir(request):
    if request.method == 'POST':
        formulario = FormularioSubir(request.POST)
        if formulario.is_valid():
            data = formulario.cleaned_data
            
            
            tipos = []
            if data['articulo']:
                tipos.append(ARTICULO)
            if data['libro']:
                tipos.append(LIBRO)
            if data['con_con']:
                tipos.append(COM_CON)

            desde= data['desde']
            hasta = data['hasta']

            google_scholar_results = []
            dblp_results = []
            ieee_results = []
            errors = []

            if data['articulo']:
                try:
                    dblp_results = xml_parser("static/dblp-pruebas.xml", "static/dblp.json", desde, hasta)
                except Exception as e:
                    errors.append(e)
                
                with open('static/dblp.json', 'w') as json_file:
                    json.dump(dblp_results, json_file)
                json_file.close()

            try:
                ieee_results = query("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn", 'static/ieeeXplore.json', tipos, desde, hasta)
            except Exception as e:
                    errors.append(e)

            with open('static/ieeeXplore.json', 'w') as json_file:
                json.dump(ieee_results, json_file)
            json_file.close()

            selenium = Selenium()

            try:
                google_scholar_results = selenium.search(
                desde, hasta, '', tipos)
            except Exception as e:
                errors.append(e)
            

            with open('static/google_scholar.json', 'w') as json_file:
                json.dump(google_scholar_results, json_file)
            json_file.close()

            con = sql_connection() 
            insert_in_database(con, PATHS)

            
            args = {
                'google_scholar_results' : len(google_scholar_results),
                'dblp_results':len(dblp_results),
                'ieee_results':len(ieee_results),
                'results': len(google_scholar_results) + len(dblp_results) + len(ieee_results),
                'errors':errors
            }
            return render(request, 'resultados_subida.html', args)
        
    else:
        formulario = FormularioSubir()


    return render(request, 'subir.html', {'formulario': formulario})


class FormularioSubir(forms.Form):
    articulo = forms.BooleanField(label='articulo',required=False)
    libro = forms.BooleanField(label='libro',required=False)
    con_con = forms.BooleanField(label='con_con',required=False)
    desde = forms.IntegerField(label='desde', min_value=1000,max_value=2020)
    hasta = forms.IntegerField(label='hasta', min_value=1000,max_value=2020)