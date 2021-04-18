import random
import sys
from email.mime.text import MIMEText
from smtplib import SMTP

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from djangoProject3.settings import EMAIL_PASS


def login_view(request):
    if request.method == 'GET':
        return render(request, 'templates/login.html', {})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return render(request, 'profile.html', {})
        else:
            return render(request, template_name='login.html', context={'error': 'login failed.'})


@login_required
def verify_email(request):
    if request.method == 'GET':
        return render(request, 'verify_email.html', context={})
    if request.method == 'POST':
        customer = request.user.customer
        customer.email_verify_code = random.randint(100000, 999999)
        customer.save()
        sender = 'arash.ataee76@yahoo.com'
        destination = [request.user.email]

        USERNAME = "arash.ataee76@yahoo.com"
        PASSWORD = EMAIL_PASS

        content = "your email verify code is: {}".format(customer.email_verify_code)

        msg = MIMEText(content, 'plain')
        msg['Subject'] = 'verify email'
        msg['From'] = sender  # some SMTP servers will do this automatically, not all

        conn = SMTP('smtp.mail.yahoo.com', 587)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

        return HttpResponseRedirect(reverse('verify-code'))


def verify_code(request):
    if request.method == 'GET':
        return render(request, 'verify_code.html', {})
    if request.method == 'POST':
        code = request.POST.get('code')
        customer = request.user.customer
        if code == customer.email_verify_code:
            customer.email_verified = True
            customer.save()
            return render(request, 'verify_code.html', {'error': 'Your email verified successfully.'})
        else:
            render(request, 'verify_code.html', {'error': 'verify email failed.'})
