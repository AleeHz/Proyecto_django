from django.db import models


from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
