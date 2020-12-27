from django.shortcuts import render


def resultados_subida(request, desde):
    return render(request, 'resultados_subida.html', {'desde': desde})
