"""
URL configuration for mi_proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import views
from django.conf import settings
from django.conf.urls.static import static
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth import logout
from django.shortcuts import redirect
from web.views import custom_logout



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registrar/', views.registrar_view, name='registrar'),
    path('homes/', views.homes, name='homes'),
    path('productos/', views.productos, name='productos'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('logout/', custom_logout, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('manual/', views.manual, name='manual'),
    path('historial/', views.historial_view, name='historial'),
    path('carrito/', views.carrito, name='carrito'),
    path('cambiar/', views.cambiar, name='cambiar'),
    path('restablecer/', views.restablecer, name='restablecer'),
    path("cambiar/<uidb64>/<token>/", views.cambiar, name="cambiar"),
    path('password_changed/', views.password_changed, name='password_changed'),
    path('send_email/', views.send_email, name='send_email'),
    path('save_purchase_history/', views.save_purchase_history, name='save_purchase_history'),
    path('eliminar_compra/<int:purchase_id>/', views.eliminar_compra, name='eliminar_compra'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    