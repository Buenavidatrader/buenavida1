from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Producto, CartItem, CustomUser, Pedido, Purchase
from django.utils.html import format_html

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'total')
    search_fields = ('usuario__username', 'fecha')
    list_filter = ('fecha',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'total', 'colored_status')
    list_filter = ('status',)
    search_fields = ('user__username', 'date', 'total')
    ordering = ('-date',)

    def colored_status(self, obj):
        if obj.status == 'pendiente':
            color = 'orange'
        elif obj.status == 'entregado':
            color = 'green'
        else:
            color = 'black'
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    colored_status.short_description = 'Estado'

admin.site.register(CartItem)
admin.site.register(CustomUser, UserAdmin)