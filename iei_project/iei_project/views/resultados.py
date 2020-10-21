from django.shortcuts import render

def resultados (request,publicaciones):
    return render(request,'resultados.html')