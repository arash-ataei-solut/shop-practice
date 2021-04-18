from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verify_code = models.CharField(max_length=100, null=True)
    email_verified = models.BooleanField(default=False)
