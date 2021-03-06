"""iei_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from bibliosearch.views.subir import subir
from bibliosearch.views.buscar import buscar
from bibliosearch.views.resultados import resultados, resultados_a, resultados_t, resultados_ta
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buscar/', buscar,name='buscar'),
    path('resultados/titulo:<str:titulo>&autor:<str:autor>&desde:<str:desde>&hasta:<str:hasta>&articulo:<str:articulo>&libro:<str:libro>&com_con:<str:com_con>', resultados_ta, name='resultados'),
    path('resultados/autor:<str:autor>&desde:<str:desde>&hasta:<str:hasta>&articulo:<str:articulo>&libro:<str:libro>&com_con:<str:com_con>', resultados_a, name='resultados'),
    path('resultados/titulo:<str:titulo>&desde:<str:desde>&hasta:<str:hasta>&articulo:<str:articulo>&libro:<str:libro>&com_con:<str:com_con>', resultados_t, name='resultados'),
    path('resultados/desde:<str:desde>&hasta:<str:hasta>&articulo:<str:articulo>&libro:<str:libro>&com_con:<str:com_con>', resultados, name='resultados'),
    path('subir/', subir,name='subir'),
]