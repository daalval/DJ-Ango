from django.db import models

# Create your models here.

class Revista(models.Model):
    id_revista = models.IntegerField(primary_key = True, null = False)
    nombre = models.CharField(null = True, max_length = 45)

class Ejemplar(models.Model):
    id_ejemplar = models.IntegerField(primary_key = True, null = False)
    volumen = models.IntegerField(null = True)
    numero = models.IntegerField(null = True)
    mes = models.IntegerField(null = True)
    revista = models.ForeignKey(Revista, on_delete = models.CASCADE)

class Publicacion(models.Model):
    id_publicacion = models.IntegerField(primary_key = True, null = False, unique=True)
    titulo = models.CharField(null = True, max_length = 45, unique=True)
    anyo = anyo = models.IntegerField(null = True)
    URL = models.CharField(null = True, max_length = 45)

class Articulo(models.Model):
    pagina_inicio = models.IntegerField(null = True)
    pagina_fin = models.IntegerField(null = True)
    ejemplar = models.ForeignKey(Ejemplar, on_delete = models.CASCADE, null = False)
    publicacion = models.OneToOneField(Publicacion, on_delete = models.CASCADE, null = False, primary_key = True)

class Com_con(models.Model):
    congreso = models.CharField(null = True, max_length = 45)
    edicion = models.CharField(null = True, max_length = 45)
    lugar = models.CharField(null = True, max_length = 45)
    pagina_inicio = models.IntegerField(null = True)
    pagina_fin = models.IntegerField(null = True)
    publicacion = models.OneToOneField(Publicacion, on_delete = models.CASCADE, null = False, primary_key = True)

class Libro(models.Model):
    editorial = models.CharField(null = True, max_length = 45)
    publicacion = models.OneToOneField(Publicacion, on_delete = models.CASCADE, null = False, primary_key = True)

class Persona(models.Model):
    id_persona = models.IntegerField(primary_key = True, null = False)
    nombre = models.CharField(null = True, max_length = 45)
    apellidos = models.CharField(null = True, max_length = 45)

    class Meta:
        unique_together = (("nombre", "apellidos"))

class PersonaPublicacion(models.Model):
    id_personapublicacion = models.IntegerField(primary_key= True, null = False)
    persona = models.ForeignKey(Persona, on_delete = models.CASCADE, null = False)
    publicacion = models.ForeignKey(Publicacion, on_delete = models.CASCADE, null = False)

    class Meta:
        unique_together = (("persona", "publicacion"))