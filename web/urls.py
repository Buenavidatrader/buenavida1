from django.urls import path
from .views import home, carrito, login_view, registrar_view, homes, productos, nosotros, contacto, perfil, manual, logout_view, carrito_view, CustomPasswordResetView, CustomPasswordResetConfirmView, procesar_pago, send_email, HomeView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('carrito/', views.cart_view, name='carrito'),
    path('login/', views.login_view, name='login'),
    path('registrar/', registrar_view, name='registrar'),
    path('homes/', views.homes_view, name='homes'),
    path('productos/', productos, name='productos'),
    path('nosotros/', nosotros, name='nosotros'),
    path('contacto/', contacto, name='contacto'),
    path('perfil/', perfil, name='perfil'),
    path('manual/', manual, name='manual'),
    path('logout/', logout_view, name='logout'),
    path('carrito_view/', carrito_view, name='carrito_view'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('send_email/', send_email, name='send_email'),
    path('api/get_cart/', views.get_cart, name='get_cart'),
    path('api/increment_quantity/', views.increment_quantity, name='increment_quantity'),
    path('api/decrement_quantity/', views.decrement_quantity, name='decrement_quantity'),
    path('api/remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
   
]