from django.shortcuts import get_object_or_404, render
import math
from bibliosearch.controllers.dbController import select_data
from bibliosearch.controllers.seleniumEngine import Selenium

MAX_ITEMS = 9
MAX_ROWS = 3


def resultados(request,titulo,autor,desde,hasta,articulo,libro,com_con,page):
    tipos = []

    if articulo:
        tipos.append('bbdd_articulo')
    if libro:
        tipos.append('bbdd_libro')
    if com_con:
        tipos.append('bbdd_com_con')
    
    full_list = full_list = select_data(titulo, autor, desde, hasta, tipos)

    print(len(full_list))

    max_page = math.ceil(len(full_list) / MAX_ITEMS)

    first_index = (page - 1) * MAX_ITEMS
    last_index = page * MAX_ITEMS

    list = full_list[first_index:last_index]

    rows = math.ceil(len(list) / MAX_ROWS)

    url_previus = f'/resultados/{titulo}/{autor}/{desde}/{hasta}/{articulo}/{libro}/{com_con}/{page - 1}' if page > 1 else None
    url_next = f'/resultados/{titulo}/{autor}/{desde}/{hasta}/{articulo}/{libro}/{com_con}/{page + 1}' if page < max_page else None

    args = {
        'list':list,
        'rows':rows,
        'url_previus':url_previus,
        'url_next':url_next,
        'page':page
    }
    
    return render(request, 'resultados.html',args)
