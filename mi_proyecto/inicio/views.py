from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, HttpResponseForbidden, JsonResponse


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

from django.contrib.auth.decorators import login_required

from .models import Post, Categoria, Comentario
from .forms import PostForm , ComentarioForm

from django.contrib.admin.views.decorators import staff_member_required

from django.views.decorators.http import require_POST

from django.utils import timezone



def inicio(request):
    posts = Post.objects.all().order_by('-fecha_publicacion')
    
    if request.user.is_authenticated:
        for post in posts:
            post.user_dio_like = request.user in post.likes.all()
    else:
        for post in posts:
            post.user_dio_like = False
    
        
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
            nuevo_post.fecha_publicacion = timezone.now()
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


@login_required
def agregar_comentario(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto:
            Comentario.objects.create(post=post, autor=request.user, texto=texto)
    
    return redirect('inicio')

@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if request.user != comentario.autor and not request.user.is_staff:
        return HttpResponseForbidden("No estás autorizado para eliminar este comentario.")

    if request.method == 'POST':
        comentario.delete()
        return redirect('inicio')
    return render(request, 'inicio/confirmar_eliminacion_comentario.html', {'comentario': comentario})

@login_required
def eliminar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.autor and not request.user.is_staff:
        return HttpResponseForbidden("No estás autorizado para eliminar este post.")

    if request.method == 'POST':
        post.delete()
        return redirect('inicio')  # o la vista que quieras después de eliminar
    return render(request, 'inicio/confirmar_eliminacion_post.html', {'post': post})


@login_required
def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.autor:
        return HttpResponseForbidden("No tenés permiso para editar este post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detalle_post', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'inicio/editar_post.html', {'form': form})

@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user != comentario.autor:
        return HttpResponseForbidden("No tenés permiso para editar este comentario.")

    if request.method == 'POST':
        comentario.texto = request.POST.get('texto')
        comentario.save()
        return redirect('inicio')
    return render(request, 'inicio/editar_comentario.html', {'comentario': comentario})


def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('login') #podria cambiar "login" por "inicio" si quiero
    else:
        form = UserCreationForm()
    return render(request, 'inicio/registro.html', {'form': form})


@login_required
@require_POST
def toggle_like_unificado(request):
    import json
    data = json.loads(request.body)
    tipo = data.get("tipo")
    objeto_id = data.get("id")

    if tipo == "post":
        objeto = Post.objects.get(id=objeto_id)
    elif tipo == "comentario":
        objeto = Comentario.objects.get(id=objeto_id)
    else:
        return JsonResponse({"error": "Tipo inválido"}, status=400)

    if request.user in objeto.likes.all():
        objeto.likes.remove(request.user)
        liked = False
    else:
        objeto.likes.add(request.user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": objeto.likes.count()
    })