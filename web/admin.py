from django.contrib import admin
from .models import Producto
from django.contrib.auth.models import User
from .models import CartItem
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'descripcion')
    search_fields = ('nombre',)

admin.site.register(CartItem)
admin.site.register(CustomUser, UserAdmin)


# Obtén el usuario "juan"
user = User.objects.get(username='juan')

# Otorga permisos de superusuario
user.is_superuser = True
user.is_staff = True
user.save()