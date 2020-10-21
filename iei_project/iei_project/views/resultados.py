from django.shortcuts import render


def resultados(request, titulo,autor,fecha,tipos,page):
    list = [1,2,3]
    return render(request, 'resultados.html' , {'list':list})
