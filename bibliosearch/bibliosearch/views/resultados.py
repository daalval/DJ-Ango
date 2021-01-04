from django.shortcuts import render
import math
from bibliosearch.controllers.dbController import select_data
from bibliosearch.controllers.seleniumEngine import Selenium

MAX_ITEMS = 9
MAX_ROWS = 3


def resultados(request):
    
    titulo = request.GET["title"]
    autor = request.GET["author"]
    fecha_ini = request.GET["fecha_ini"]
    fecha_fin = request.GET["fecha_fin"]

    tipos = []

    if request.GET["check_articulo"] == 'value':
        tipos.append('bbdd_articulo')

    if request.GET["check_book"] == 'value':
        tipos.append('bbdd_libro')

    if request.GET["check_con"] == 'value':
        tipos.append('bbdd_com_con')
    
    data = select_data(titulo, autor, fecha_ini, fecha_fin, tipos)
    print(data)
    return render(request, 'resultados.html')
