from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

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


from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    return render(request, 'inicio/admin_dashboard.html')

@login_required
def usuario_dashboard(request):
    return render(request, 'inicio/usuario_dashboard.html')
<<<<<<< HEAD

=======
>>>>>>> 4c872381eb5f2ff4499f79352ecfad2e8ad62839
