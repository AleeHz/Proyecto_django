from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('usuario-dashboard/', views.usuario_dashboard, name='usuario_dashboard'),
]
