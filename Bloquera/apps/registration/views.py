from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    error_message = None 
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is None:
            error_message = "Nombre de usuario o contraseña incorrectos."  
        else:
            login(request, user)
            return redirect('estadisticas:estadisticas')

    return render(request, 'registration/login.html', {'error_message': error_message})
