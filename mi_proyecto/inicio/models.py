from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Post(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes_post', blank=True)
    imagen = models.ImageField(upload_to='posts_imagenes/', blank=True, null=True)
    

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    post = models.ForeignKey(Post, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comentarios_likes', blank=True)
    

    def __str__(self):
        return f"{self.autor.username} - {self.texto[:20]}"
    
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatares/', default='avatares/default.png')

    def __str__(self):
        return f'Perfil de {self.user.username}'
