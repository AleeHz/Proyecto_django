from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


from django.contrib.auth.decorators import login_required

from .models import Post, Categoria, Comentario
from .forms import PostForm , ComentarioForm


def inicio(request):
    posts = Post.objects.all().order_by('-fecha_creacion')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.post = Post.objects.get(pk=request.POST.get('post_id'))
            comentario.save()
            return redirect('inicio')
    else:
        form = ComentarioForm()

    return render(request, 'inicio/inicio.html', {
        'posts': posts,
        'form': form,
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            
            if usuario.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('usuario_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'inicio/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def perfil(request):
    if request.user.is_superuser:
        base_template = 'inicio/base_admin.html'
    else:
        base_template = 'inicio/base_usuario.html'
    
    return render(request, 'inicio/perfil.html', {
        'base_template': base_template
    })

def perfil_view(request):
    return render(request, 'inicio/perfil.html')


@login_required
def admin_dashboard(request):
    return render(request, 'inicio/admin_dashboard.html')

@login_required
def usuario_dashboard(request):
    return render(request, 'inicio/usuario_dashboard.html')



@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            nuevo_post = form.save(commit=False)
            nuevo_post.autor = request.user  # ← asigna el autor automáticamente
            nuevo_post.save()
            return redirect('lista_posts')  # cambiá esto por el nombre correcto si es distinto
    else:
        form = PostForm()
    return render(request, 'inicio/crear_post.html', {'form': form})

@login_required
def lista_posts(request):
    posts = Post.objects.all()
    return render(request, 'inicio/lista_posts.html', {'posts': posts})


@login_required
def detalle_post(request, post_id):
    post = Post.objects.get(id=post_id)
    comentarios = post.comentarios.all().order_by('-fecha')  # gracias al related_name
    return render(request, 'inicio/detalle_post.html', {
        'post': post,
        'comentarios': comentarios
    })