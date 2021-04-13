from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()


class Cart(models.Model):
    STATUS_CHOICES = {
        ('OPEN', 'open'),
        ('CLOSED', 'closed')
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', related_query_name='cart')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='open')


class CartItem(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts', related_query_name='cart')
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', related_query_name='item')
