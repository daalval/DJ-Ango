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
    
    # full_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # max_page = math.ceil(len(full_list) / MAX_ITEMS)

    # first_index = (page - 1) * MAX_ITEMS
    # last_index = (page * MAX_ITEMS) - 1

    # list = full_list[first_index:last_index]

    # rows = math.ceil(len(list) / MAX_ROWS)

    # url_previus = f"/resultados/{titulo}/{autor}/{fecha}/{tipos}/{page - 1}/" if page > 1 else None
    # url_next = f"/resultados/{titulo}/{autor}/{fecha}/{tipos}/{page + 1}/" if page < max_page else None

    # return render(request, 'resultados.html', {'list': list, 'page': page, 'max_page': max_page, 'titulo': titulo, 'autor': autor, 'fecha': fecha, 'tipos': tipos, 'url_previus': url_previus, 'url_next': url_next,'rows':rows})
