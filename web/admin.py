from django.contrib import admin
from .models import Producto
from django.contrib.auth.models import User
from .models import CartItem
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Pedido


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'total')
    search_fields = ('usuario__username', 'fecha')
    list_filter = ('fecha',)

admin.site.register(CartItem)
admin.site.register(CustomUser, UserAdmin)


# Obtén el usuario "juan"
user = User.objects.get(username='juan')

# Otorga permisos de superusuario
user.is_superuser = True
user.is_staff = True
user.save()