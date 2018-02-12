from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Concurso(models.Model):

    # Definicion atributos

    nombre = models.CharField(max_length=200)
    ruta_imagen = models.ImageField(max_length=500)
    url_concurso = models.URLField(max_length=200)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    valor_pagar = models.FloatField(max_length=200)
    texto_voz = models.CharField(max_length=2000)
    recomendaciones = models.CharField(max_length=2000)
    estado = models.CharField(max_length=2000)
    id_administrador = models.ForeignKey(User,on_delete=models.CASCADE)

#class Audio(models.Model):


    #archivo_original = models.FileField


class Locutor(models.Model):

    # Definicion atributos

    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    #id_audio = models.ForeignKey(Audio,on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=2000)
