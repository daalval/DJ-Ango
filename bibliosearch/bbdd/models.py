from django.db import models
from django.db.models import constraints

# Create your models here.

class Revista(models.model):
    idRevista = models.IntegerField(primary_key = True, null = False)
    nombre = models.CharField(null = True)

class Ejemplar(models.model):
    idEjemplar = models.IntegerField(primary_key = True, null = False)
    volumen = models.IntegerField(null = True)
    numero = models.IntegerField(null = True)
    mes = models.IntegerField(null = True)
    revista_idRevista = models.IntegerField(null = False)
    fk_Ejemplar_Revista1_idx = models.Index(revista_idRevista)
    fk_Ejemplar_Revista1 = models.ForeignKey(Revista, on_delete = models.CASCADE)

class Publicacion(models.model):
    idPublicacion = models.IntegerField(primary_key = True, null = False)
    titulo = models.CharField(null = True)
    anyo = anyo = models.IntegerField(null = True)
    URL = models.CharField(null = True)

class Articulo(models.model):
    pagina_inicio = models.IntegerField(null = True)
    pagina_fin = models.IntegerField(null = True)
    ejemplar_idEjemplar = models.IntegerField(null = False)
    publicacion_idPublicacion = models.IntegerField(null = False)
    fk_Articulo_Ejemplar1_idx = models.Index(ejemplar_idEjemplar)
    fk_Articulo_Publicacion1_idx = models.Index(publicacion_idPublicacion)
    fk_Articulo_Ejemplar1 = models.ForeignKey(Ejemplar, on_delete = models.CASCADE)
    fk_Articulo_Publicacion1 = models.ForeignKey(Publicacion, on_delete = models.CASCADE)

class Com_con(models.model):
    congreso = models.CharField(null = True)
    edicion = models.CharField(null = True)
    lugar = models.CharField(null = True)
    pagina_inicio = models.IntegerField(null = True)
    pagina_fin = models.IntegerField(null = True)
    publicacion_idPublicacion = models.IntegerField(null = False)
    fk_Articulo_Publicacion1_idx = models.Index(publicacion_idPublicacion)
    fk_Articulo_Publicacion1 = models.ForeignKey(Publicacion, on_delete = models.CASCADE)

class Libro(models.model):
    editorial = models.CharField(null = True)