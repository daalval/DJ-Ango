from django.shortcuts import render

def buscar (request,publicaciones):
    return render(request,'buscar.html')