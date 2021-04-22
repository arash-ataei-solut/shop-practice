from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, related_name='child',
        related_query_name='child'
    )


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)

    @property
    def num_of_cart_item(self):
        return self.carts.count()


class Cart(models.Model):
    STATUS_CHOICES = {
        ('OPEN', 'open'),
        ('CLOSED', 'closed')
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', related_query_name='cart')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='open')


class CartItem(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts', related_query_name='cart')
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', related_query_name='item')
