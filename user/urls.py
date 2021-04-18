from django.contrib.auth.views import LoginView
from django.urls import path

from user.views import verify_email, login_view, verify_code

urlpatterns = [
    path('login/', login_view, name='login'),
    path('verify-email/', verify_email, name='verify-email'),
    path('verify-code/', verify_code, name='verify-code')
]