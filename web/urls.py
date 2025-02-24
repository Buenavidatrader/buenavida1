from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registrar/', views.registrar_view, name='registrar'),
    path('homes/', views.homes, name='homes'),
    path('productos/', views.productos, name='productos'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('logout/', views.logout_view, name='logout'),
    path('manual/', views.manual, name='manual'),
    path('carrito/', views.carrito, name='carrito'),
    
]