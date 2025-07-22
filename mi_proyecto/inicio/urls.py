from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),


    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('usuario-dashboard/', views.usuario_dashboard, name='usuario_dashboard'),

    
    path('inicio/', views.inicio, name='inicio'),
    path('perfil/', views.perfil, name='perfil'),
    path('crear-post/', views.crear_post, name='crear_post'),
    path('lista-posts/', views.lista_posts, name='lista_posts'),

    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),

]
