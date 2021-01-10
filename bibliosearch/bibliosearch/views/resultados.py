from bibliosearch.models.Publicacion import Publicacion
from django.shortcuts import get_object_or_404, render
import math
from bibliosearch.controllers.dbController import select_data
from bibliosearch.controllers.googleScholar_extractor import Selenium
from django.core.paginator import Paginator

MAX_ITEMS = 9
MAX_ROWS = 3

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
