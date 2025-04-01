from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import Producto, CustomUser, CartItem, PurchaseHistory, Purchase, PurchaseItem
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pedido
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    if request.path.startswith('/admin/'):
        # No cerrar sesión del admin
        return redirect('/admin/')
    return redirect('/')

logger = logging.getLogger(__name__)

@login_required
def save_purchase_history(request):
    if request.method == 'POST':
        cart_summary = request.POST.get('cart_summary')
        cart = json.loads(request.POST.get('cart'))
        total = request.POST.get('total')
        user_email = request.user.email
        company_email = 'jsbplaza@gmail.com'  # Reemplaza con el correo de la empresa

        # Enviar correo al usuario y a la empresa
        send_mail(
            'Resumen de tu compra en BuenaVida',
            cart_summary,
            'jsbplaza@gmail.com',  # Reemplaza con tu dirección de correo real
            [user_email, company_email],  # Lista de destinatarios
            fail_silently=False,
        )

        # Guardar el historial de compra en la base de datos
        purchase = Purchase.objects.create(user=request.user, ñtotal=total)
        for item in cart:
            PurchaseItem.objects.create(
                purchase=purchase,
                name=item['name'],
                quantity=item['quantity'],
                total_price=item['price'] * item['quantity']
            )

        return JsonResponse({'message': 'Compra guardada y correos enviados correctamente.'})

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

@login_required
def historial_view(request):
    # Obtén el historial de compras del usuario actual
    purchase_history = Purchase.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'historial.html', {'purchase_history': purchase_history})

def home(request):
    return render(request, 'home.html')

def historial(request):
    return render(request, 'historial.html')

def carrito(request):
    return render(request, 'carrito.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario no registrado. Por favor, regístrese para poder acceder.')
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

        # Enviar correo a la empresa
        send_mail(
            f'Mensaje de {nombre} desde el formulario de contacto',
            mensaje,
            email,
            ['jsbplaza@gmail.com'],
            fail_silently=False,
        )

        # Enviar correo de confirmación al usuario
        send_mail(
            'Confirmación de recepción de mensaje',
            f'Hola {nombre},\n\nHemos recibido tu mensaje:\n\n"{mensaje}"\n\nNos pondremos en contacto contigo pronto.\n\nSaludos,\nEquipo BuenaVida',
            'info@buenavida.com',  # Correo del remitente
            [email],  # Correo del destinatario
            fail_silently=False,
        )

        messages.success(request, 'Tu mensaje ha sido enviado exitosamente. Revisa tu correo para la confirmación.')
        return redirect('contacto')

    return render(request, 'contacto.html')

@login_required
def perfil(request):
    purchase_history = PurchaseHistory.objects.filter(user=request.user)
    return render(request, 'perfil.html', {'purchase_history': purchase_history})

def manual(request):
    return render(request, 'manual.html')

def restablecer(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            enlace = request.build_absolute_uri(f"/cambiar/{uid}/{token}/")
            send_mail(
                "Restablecimiento de contraseña",
                f"Haz clic en el siguiente enlace para cambiar tu contraseña: {enlace}",
                "jsbplaza@gmail.com",
                [email],
                fail_silently=False,
            )
            messages.success(request, "Se ha enviado un enlace a tu correo para restablecer tu contraseña")
        else:
            messages.error(request, "No existe un usuario con ese correo")
            return redirect("home")
    return render(request, "restablecer.html")

def cambiar(request):
    return render(request, 'cambiar.html')

def password_changed(request):
    return render(request, 'password_changed.html')

def logout_view(request):
    user_name = request.user.username
    logout(request)

    return redirect('home')  # Redirige a la página de inicio

@csrf_protect
def my_view(request):
    return render(request, 'my_template.html', {})

def carrito_view(request):
    context = {
        'user': request.user,
    }
    return render(request, 'carrito.html', context)

def cambiar (request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            nueva_contraseña = request.POST["password"]
            user.set_password(nueva_contraseña)
            user.save()
            return redirect("password_changed")
        
        return render(request, "cambiar.html")
    return redirect("login")

def send_email(request):
    if request.method == 'POST':
        cart_summary = request.POST.get('cart_summary')
        user_email = request.user.email  # Asumiendo que el usuario está autenticado y tiene un email
        company_email = 'jsbplaza@gmail.com'  # Reemplaza con el correo de la empresa

        send_mail(
            'Resumen de tu compra',
            cart_summary,
            settings.DEFAULT_FROM_EMAIL,
            [user_email, company_email],  # Enviar a ambos correos
            fail_silently=False,
        )
        return redirect('carrito')  # Redirigir a la página del carrito después de enviar el correo
    return render(request, 'carrito.html')

@login_required
def get_cart(request):
    user = request.user
    return JsonResponse(user.cart, safe=False)

@csrf_exempt
@login_required
def increment_quantity(request):
    user = request.user
    data = json.loads(request.body)
    index = data['index']
    user.cart[index]['quantity'] += 1
    user.save()
    return JsonResponse({'status': 'success'})

@csrf_exempt
@login_required
def decrement_quantity(request):
    user = request.user
    data = json.loads(request.body)
    index = data['index']
    if user.cart[index]['quantity'] > 1:
        user.cart[index]['quantity'] -= 1
        user.save()
    return JsonResponse({'status': 'success'})

@csrf_exempt
@login_required
def remove_from_cart(request):
    user = request.user
    data = json.loads(request.body)
    index = data['index']
    user.cart.pop(index)
    user.save()
    return JsonResponse({'status': 'success'})

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'carrito.html', {'cart_items': cart_items})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import CartItem
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product_name = data.get('product_name')
        quantity = data.get('quantity')
        price = data.get('price')

        # Lógica para agregar el producto al carrito
        # ...

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def eliminar_producto_historial(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        purchase_id = data.get('purchase_id')
        item_index = data.get('item_index')

        purchase = get_object_or_404(Purchase, id=purchase_id)
        items = list(purchase.items.all())

        if 0 <= item_index < len(items):
            item = items[item_index]
            item.delete()

            if not purchase.items.exists():
                purchase.delete()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Índice de producto no válido.'})
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})

class CheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        cart = request.POST.get('cart')
        total = request.POST.get('total')
        detalles = request.POST.get('detalles')

        pedido = Pedido.objects.create(
            usuario=request.user,
            total=total,
            detalles=detalles
        )

        # Limpiar el carrito después de la compra
        request.session['cart'] = []

        return redirect('success')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Purchase

@login_required
def historial_view(request):
    purchase_history = Purchase.objects.filter(user=request.user)
    return render(request, 'historial.html', {'purchase_history': purchase_history})

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Purchase

@login_required
def eliminar_compra(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user)
    purchase.delete()
    return redirect('historial')



def historial_view(request):
    # Fetch purchase history for the current user
    purchase_history = Purchase.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'historial.html', {'purchase_history': purchase_history})


def save_purchase_history(request):
    if request.method == 'POST':
        cart_data = request.POST.get('cart')
        total = request.POST.get('total')
        
        # Create a new Purchase
        purchase = Purchase.objects.create(
            user=request.user,
            total=float(total),
            status='pendiente'
        )
        
        # Parse the cart data
        cart_items = json.loads(cart_data)
        
        # Create PurchaseItems
        for item in cart_items:
            PurchaseItem.objects.create(
                purchase=purchase,
                name=item['name'],
                quantity=item['quantity'],
                unit_price=item['price'],
                total_price=item['price'] * item['quantity']
            )
        
        return redirect('historial')




