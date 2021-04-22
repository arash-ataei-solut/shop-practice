import datetime
import random
import sys
from email.mime.text import MIMEText
from smtplib import SMTP

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.models import VerifyCode


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            request.session['name'] = user.username
            print(request.session['name'])
            response = render(request, 'profile.html', {'session': request.session['name']})
            response.set_cookie('name', user.username)
            return response

        else:
            return render(request, template_name='login.html', context={'error': 'login failed.'})


@login_required
def verify_email(request):
    if request.method == 'GET':
        return render(request, 'verify_email.html', context={})
    if request.method == 'POST':
        customer = request.user.customer
        verify_code, created = VerifyCode.objects.get_or_create(customer=customer)
        verify_code.code = random.randint(100000, 999999)
        print(datetime.datetime.now() + datetime.timedelta(minutes=1))
        verify_code.expire = datetime.datetime.now() + datetime.timedelta(minutes=1)
        verify_code.save()
        customer.save()
        # sender = 'arash.ataee76@yahoo.com'
        # destination = [request.user.email]
        #
        # USERNAME = "arash.ataee76@yahoo.com"
        # PASSWORD = 'EMAIL_PASS'
        #
        # content = "your email verify code is: {}".format(customer.email_verify_code)
        #
        # msg = MIMEText(content, 'plain')
        # msg['Subject'] = 'verify email'
        # msg['From'] = sender  # some SMTP servers will do this automatically, not all
        #
        # conn = SMTP('smtp.mail.yahoo.com', 587)
        # conn.set_debuglevel(False)
        # conn.login(USERNAME, PASSWORD)
        # try:
        #     conn.sendmail(sender, destination, msg.as_string())
        # finally:
        #     conn.quit()

        send_mail(
            'email', str(customer.verifycode.code),
            'arash.ataea76@gmail.com', [request.user.email],
            fail_silently=False
        )

        return HttpResponseRedirect(reverse('verify-code'))


def verify_code_view(request):
    if request.method == 'GET':
        return render(request, 'verify_code.html', {})
    if request.method == 'POST':
        code = request.POST.get('code')
        customer = request.user.customer
        if code == customer.verifycode.code and customer.verifycode.expire <= datetime.datetime.now():
            customer.email_verified = True
            customer.save()
            return render(request, 'verify_code.html', {'error': 'Your email verified successfully.'})
        else:
            return render(request, 'verify_code.html', {'error': 'verify email failed.'})
