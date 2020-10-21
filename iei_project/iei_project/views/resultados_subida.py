from django.shortcuts import render


def resultados_subida(request,articulo,libro,com_con,fecha):
    return render(request, 'resultados_subida.html')
