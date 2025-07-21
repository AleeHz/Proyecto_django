from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
<<<<<<< HEAD
    path('logout/', views.logout_view, name='logout'),
=======
>>>>>>> 4c872381eb5f2ff4499f79352ecfad2e8ad62839
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('usuario-dashboard/', views.usuario_dashboard, name='usuario_dashboard'),
]
