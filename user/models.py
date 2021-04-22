from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)


class VerifyCode(models.Model):
    code = models.CharField(max_length=100)
    expire = models.DateTimeField(null=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True)
