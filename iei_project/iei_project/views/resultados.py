from django.shortcuts import render


def resultados(request, publicaciones):
    print(publicaciones)
    return render(request, 'resultados.html')
