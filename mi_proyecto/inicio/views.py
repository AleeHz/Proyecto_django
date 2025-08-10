from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, HttpResponseForbidden, JsonResponse


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

from django.contrib.auth.decorators import login_required

from .models import Post, Categoria, Comentario,Perfil
from .forms import PostForm , ComentarioForm  , AvatarForm

from django.contrib.admin.views.decorators import staff_member_required

from django.views.decorators.http import require_POST

from django.utils import timezone

from django.contrib.auth.models import User


from django.contrib import messages

from django.urls import reverse

from django.shortcuts import get_object_or_404


import json

from django.db.models import Q

#tengo q ver esto aun no funciona bien
def inicio(request):
    # Tomamos el valor del filtro de la URL 
    filtro = request.GET.get('filtro', '')

    # Base query
    posts = Post.objects.all()

    # Aplicamos el filtro
    if filtro == 'fecha_asc':
        posts = posts.order_by('fecha_publicacion')
    elif filtro == 'fecha_desc':
        posts = posts.order_by('-fecha_publicacion')
    elif filtro == 'con_imagen':
        posts = posts.exclude(imagen='').order_by('-fecha_publicacion')
    else:
        posts = posts.order_by('-fecha_publicacion')

    # Añadimos flags para saber si el usuario dio like
    if request.user.is_authenticated:
        for post in posts:
            post.user_dio_like = request.user in post.likes.all()
            for comentario in post.comentarios.all():
                comentario.user_dio_like = request.user in comentario.likes.all()
    else:
        for post in posts:
            post.user_dio_like = False
            for comentario in post.comentarios.all():
                comentario.user_dio_like = False

    # Manejo de comentarios
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['texto'].strip()
            if not texto:
                messages.error(request, "El comentario no puede estar vacío.")
            else:
                comentario = form.save(commit=False)
                comentario.autor = request.user
                comentario.post = get_object_or_404(Post, pk=request.POST.get('post_id'))
                comentario.texto = texto
                comentario.save()
                return redirect('inicio')
    else:
        form = ComentarioForm()

    return render(request, 'inicio/inicio.html', {
        'posts': posts,
        'form': form,
        'filtro': filtro,
    })


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def perfil(request):
    base_template = 'inicio/base_admin.html' if request.user.is_superuser else 'inicio/base_usuario.html'

    # Perfil
    perfil, _ = Perfil.objects.get_or_create(user=request.user)

    # Actualizar avatar
    if request.method == 'POST' and 'avatar' in request.FILES:
        form = AvatarForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Avatar actualizado correctamente.")
            return redirect('mi_perfil')
    else:
        form = AvatarForm(instance=perfil)

    # Filtro
    filtro = request.GET.get("filtro")

    posts = Post.objects.filter(autor=request.user).prefetch_related('comentarios__autor')

    if filtro == "fecha_asc":
        posts = posts.order_by("fecha_publicacion")
    elif filtro == "fecha_desc":
        posts = posts.order_by("-fecha_publicacion")
    elif filtro == "con_imagen":
        posts = posts.exclude(imagen="").exclude(imagen__isnull=True).order_by("-fecha_publicacion")
    else:
        posts = posts.order_by("-fecha_publicacion")  # por defecto más recientes

    # Marcar si el usuario dio like
    for post in posts:
        post.user_dio_like = request.user in post.likes.all()

    # Formulario de comentario
    comentario_form = ComentarioForm()

    return render(request, 'inicio/perfil.html', {
        'perfil': perfil,
        'form': form,
        'posts': posts,
        'comentario_form': comentario_form,
        'base_template': base_template,
    })


def perfil_usuario(request, username):
    usuario = get_object_or_404(User, username=username)
    posts = Post.objects.filter(autor=usuario)

    filtro = request.GET.get('filtro')  # fecha_desc, fecha_asc, con_imagen, sin_imagen
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if filtro == 'con_imagen':
        posts = posts.exclude(Q(imagen='') | Q(imagen__isnull=True))
    elif filtro == 'sin_imagen':
        posts = posts.filter(Q(imagen='') | Q(imagen__isnull=True))

    if filtro == 'fecha_asc':
        posts = posts.order_by('fecha_publicacion')
    else:  # por defecto fecha_desc
        posts = posts.order_by('-fecha_publicacion')

    if fecha_inicio:
        posts = posts.filter(fecha_publicacion__date__gte=fecha_inicio)
    if fecha_fin:
        posts = posts.filter(fecha_publicacion__date__lte=fecha_fin)

    # Likes
    if request.user.is_authenticated:
        for post in posts:
            post.user_dio_like = request.user in post.likes.all()
            for comentario in post.comentarios.all():
                comentario.user_dio_like = request.user in comentario.likes.all()
    else:
        for post in posts:
            post.user_dio_like = False
            for comentario in post.comentarios.all():
                comentario.user_dio_like = False

    # Comentarios
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['texto'].strip()
            if not texto:
                messages.error(request, "El comentario no puede estar vacío.")
            else:
                comentario = form.save(commit=False)
                comentario.autor = request.user
                comentario.post = get_object_or_404(Post, pk=request.POST.get('post_id'))
                comentario.texto = texto
                comentario.save()
                return redirect('perfil_usuario', username=username)
    else:
        form = ComentarioForm()

    perfil = getattr(usuario, 'perfil', None)
    base_template = 'inicio/base_admin.html' if request.user.is_superuser else 'inicio/base_usuario.html'

    return render(request, 'inicio/perfil_usuario.html', {
        'usuario_perfil': usuario,
        'posts': posts,
        'base_template': base_template,
        'perfil': perfil,
        'comentario_form': form,
        'filtro': filtro,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })





@login_required
def admin_dashboard(request):
    return render(request, 'inicio/admin_dashboard.html')

@login_required
def usuario_dashboard(request):
    return render(request, 'inicio/usuario_dashboard.html')



@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            titulo = form.cleaned_data['titulo'].strip()
        contenido = form.cleaned_data['contenido'].strip()
        if not titulo or not contenido:
            from django.contrib import messages
            messages.error(request, "El título y contenido no pueden estar vacíos.")
        else:
            nuevo_post = form.save(commit=False)
            nuevo_post.autor = request.user
            nuevo_post.titulo = titulo
            nuevo_post.contenido = contenido
            nuevo_post.fecha_publicacion = timezone.now()
            nuevo_post.save()
            return redirect('lista_posts')
    else:
        form = PostForm()
    return render(request, 'inicio/crear_post.html', {'form': form})

@login_required
def lista_posts(request):
    posts = Post.objects.all()
    return render(request, 'inicio/lista_posts.html', {'posts': posts})


@login_required
def detalle_post(request, post_id):
    
    if request.user.is_superuser:
        base_template = "inicio/base_admin.html"
    else:
        base_template = "inicio/base_usuario.html"
    
    post = get_object_or_404(Post, id=post_id)
    comentarios = Comentario.objects.filter(post=post).order_by('-fecha_publicacion')
    return render(request, "inicio/detalle_post.html", {
        "post": post,
        "base_template": base_template,
        "comentarios": comentarios
    })


@login_required
def agregar_comentario(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        texto = request.POST.get('comentario')
        if texto:
            Comentario.objects.create(
                post=post,
                autor=request.user,
                texto=texto
            )

    next_url = request.POST.get('next', reverse('inicio'))
    return redirect(next_url)


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
        return redirect('inicio')  
    return render(request, 'inicio/confirmar_eliminacion_post.html', {'post': post})


@login_required
def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Solo autor o superusuario pueden editar
    if request.user != post.autor and not request.user.is_superuser:
        return HttpResponseForbidden("No tenés permiso para editar este post.")

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES ,instance=post)
        if form.is_valid():
            titulo = form.cleaned_data['titulo'].strip()
            contenido = form.cleaned_data['contenido'].strip()
            if not titulo or not contenido:
            
                messages.error(request, "El título y contenido no pueden estar vacíos.")
            else:
                
                form.save()  # guarda también imagen si se usa
                return redirect('perfil_usuario', username=post.autor.username)
    else:
        form = PostForm(instance=post)

    # Elege la plantilla base según tipo de usuario
    if request.user.is_superuser:
        base_template = 'inicio/base_admin.html'
    else:
        base_template = 'inicio/base_usuario.html'

    return render(request, 'inicio/editar_post.html', {
        'form': form,
        'post': post,
        'base_template': base_template,
    })

@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user != comentario.autor:
        return HttpResponseForbidden("No tenés permiso para editar este comentario.")

    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()
    if texto:
        comentario.texto = texto
        comentario.save()
    else:
        from django.contrib import messages
        messages.error(request, "El comentario no puede estar vacío.")
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
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, TypeError):
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    tipo = payload.get('tipo')
    try:
        objeto_id = int(payload.get('id', 0))
    except (ValueError, TypeError):
        return JsonResponse({'error': 'ID inválido'}, status=400)

    if not tipo or not objeto_id:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    if tipo == 'post':
        obj = get_object_or_404(Post, id=objeto_id)
    elif tipo == 'comentario':
        obj = get_object_or_404(Comentario, id=objeto_id)
    else:
        return JsonResponse({'error': 'Tipo inválido'}, status=400)

    if request.user in obj.likes.all():
        obj.likes.remove(request.user)
        liked = False
    else:
        obj.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': obj.likes.count()
    })



def buscar_perfil(request):
    if request.method == "GET":
        query = request.GET.get("q", "").strip()

        if not query:
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # Buscar usuario
        try:
            usuario = User.objects.get(username__iexact=query)
        except User.DoesNotExist:
            return render(request, "inicio/usuario_no_encontrado.html", {"query": query})

        # Si es el usuario logueado, ir a su propio perfil
        if usuario == request.user:
            return redirect("mi_perfil")

        # Si es otro, ir a perfil_usuario
        return redirect(reverse("perfil_usuario", args=[usuario.username]))
