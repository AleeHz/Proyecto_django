from django.contrib import admin

from django.urls import path
from . import views

from .views import registro_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('usuario-dashboard/', views.usuario_dashboard, name='usuario_dashboard'),

    path('inicio/', views.inicio, name='inicio'),
    path('mi-perfil/', views.perfil, name='mi_perfil'),
    path('perfil/<str:username>/', views.perfil_usuario, name='perfil_usuario'),
    path('crear-post/', views.crear_post, name='crear_post'),
    
    
    path('lista-posts/', views.lista_posts, name='lista_posts'),

    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),

    path('comentario/<int:post_id>/', views.agregar_comentario, name='agregar_comentario'),

    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('eliminar_post/<int:post_id>/', views.eliminar_post, name='eliminar_post'),

    path('registro/', registro_view, name='register'),

    path('editar_post/<int:post_id>/', views.editar_post, name='editar_post'),
    path('editar_comentario/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),

    path("toggle_like/", views.toggle_like_unificado, name="toggle_like_unificado"),

    path("buscar/", views.buscar_perfil, name="buscar_perfil"),

    ]
