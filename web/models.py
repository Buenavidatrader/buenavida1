from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
import jsonfield

class CustomUser(AbstractUser):
    cart = jsonfield.JSONField(default=list)
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='CarritoProducto')

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en el carrito de {self.carrito.usuario.username}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)  # Asegúrate de que el producto con ID 1 exista
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    items = models.JSONField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase on {self.date} by {self.user.username}"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


