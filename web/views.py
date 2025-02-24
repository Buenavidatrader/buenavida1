from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from .models import Producto, Carrito, CarritoProducto

def home(request):
    return render(request, 'home.html')

def carrito(request):
    return render(request, 'carrito.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('homes')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
            return redirect('login')
    return render(request, 'login.html')

def registrar_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('registrar')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return redirect('registrar')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Cuenta creada exitosamente')
        return redirect('login')
    
    return render(request, 'registrar.html')

def homes(request):
    return render(request, 'homes.html')

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

def nosotros(request):
    return render(request, 'nosotros.html')

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')

        send_mail(
            f'Mensaje de {nombre} desde el formulario de contacto',
            mensaje,
            email,
            ['jsbplaza@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, 'Tu mensaje ha sido enviado exitosamente.')
        return redirect('contacto')

    return render(request, 'contacto.html')

def perfil(request):
    return render(request, 'perfil.html')

def manual(request):
    return render(request, 'manual.html')

def logout_view(request):
    auth_logout(request)
    return redirect('home')  # Redirige a la página de inicio después de cerrar sesión

