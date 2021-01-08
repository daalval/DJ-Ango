from bibliosearch.models.Publicacion import Publicacion
from django.shortcuts import get_object_or_404, render
import math
from bibliosearch.controllers.dbController import select_data
from bibliosearch.controllers.seleniumEngine import Selenium
from django.core.paginator import Paginator

MAX_ITEMS = 9
MAX_ROWS = 3


# def resultados(request,titulo,autor,desde,hasta,articulo,libro,com_con,page):
#     tipos = []

#     if articulo:
#         tipos.append('bbdd_articulo')
#     if libro:
#         tipos.append('bbdd_libro')
#     if com_con:
#         tipos.append('bbdd_com_con')
    
#     full_list = full_list = select_data(titulo, autor, desde, hasta, tipos)

#     print(len(full_list))

#     max_page = math.ceil(len(full_list) / MAX_ITEMS)

#     first_index = (page - 1) * MAX_ITEMS
#     last_index = page * MAX_ITEMS

#     list = full_list[first_index:last_index]

#     rows = math.ceil(len(list) / MAX_ROWS)

#     url_previus = f'/resultados/{titulo}/{autor}/{desde}/{hasta}/{articulo}/{libro}/{com_con}/{page - 1}' if page > 1 else None
#     url_next = f'/resultados/{titulo}/{autor}/{desde}/{hasta}/{articulo}/{libro}/{com_con}/{page + 1}' if page < max_page else None

#     args = {
#         'list':list,
#         'rows':rows,
#         'url_previus':url_previus,
#         'url_next':url_next,
#         'page':page
#     }
    
#     return render(request, 'resultados.html',args)

def resultados_ta(request,titulo,autor,desde,hasta,articulo,libro,com_con):
    tipos = []

    if articulo == 'True':
        tipos.append('bbdd_articulo')
    if libro == 'True':
        tipos.append('bbdd_libro')
    if com_con == 'True':
        tipos.append('bbdd_com_con')
    
    publicaciones = select_data(titulo, autor, desde, hasta, tipos)

    paginator = Paginator(publicaciones, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    args = {
        'page_obj': page_obj
    }
    return render(request,'resultados.html',args)

def resultados_t(request,titulo,desde,hasta,articulo,libro,com_con):
    tipos = []

    if articulo == 'True':
        tipos.append('bbdd_articulo')
    if libro == 'True':
        tipos.append('bbdd_libro')
    if com_con == 'True':
        tipos.append('bbdd_com_con')
    
    publicaciones = select_data(titulo, '', desde, hasta, tipos)

    paginator = Paginator(publicaciones, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    args = {
        'page_obj': page_obj
    }
    return render(request,'resultados.html',args)

def resultados_a(request,autor,desde,hasta,articulo,libro,com_con):
    tipos = []

    if articulo == 'True':
        tipos.append('bbdd_articulo')
    if libro == 'True':
        tipos.append('bbdd_libro')
    if com_con == 'True':
        tipos.append('bbdd_com_con')
    
    publicaciones = select_data('', autor, desde, hasta, tipos)

    paginator = Paginator(publicaciones, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    args = {
        'page_obj': page_obj
    }
    return render(request,'resultados.html',args)

def resultados(request,desde,hasta,articulo,libro,com_con):
    tipos = []

    if articulo == 'True':
        tipos.append('bbdd_articulo')
    if libro == 'True':
        tipos.append('bbdd_libro')
    if com_con == 'True':
        tipos.append('bbdd_com_con')
    
    print(tipos)
    
    publicaciones = select_data('', '', desde, hasta, tipos)

    print(len(publicaciones))
    for publicacion in publicaciones:
        print(publicacion.get_type)

    paginator = Paginator(publicaciones, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    args = {
        'page_obj': page_obj
    }
    return render(request,'resultados.html',args)
