

from django import forms
from .models import Post , Comentario , Perfil


class PostForm(forms.ModelForm):
    titulo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Escribe un título...',
            'maxlength': '100',  # frontend
            'id': 'id_titulo'
        })
    )
    contenido = forms.CharField(
        max_length=300,
        widget=forms.Textarea(attrs={
            'placeholder': 'Contenido del post...',
            'rows': 5,
            'maxlength': '300',
            'id': 'id_contenido'
        })
    )

    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'categoria', 'imagen']  # y otros si tenés


class ComentarioForm(forms.ModelForm):
    contenido = forms.CharField(
        max_length=300,
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe un comentario...',
            'rows': 3,
            'maxlength': '300',
            'id': 'id_comentario'
        })
    )

    class Meta:
        model = Comentario
        fields = ['contenido']

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['avatar']