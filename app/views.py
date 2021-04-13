from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from app.models import Product, Cart, CartItem


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return render(request, 'profile.html', {})
        else:
            return render(request, template_name='login.html', context={'error': 'login failed.'})


def add_product(request):
    if request.method == 'GET':
        return render(request, 'add_product.html', {})
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        try:
            Product.objects.create(name=name, quantity=quantity)
            return render(request, 'add_product.html', {'error': 'product created successfully'})
        except ValueError:
            return render(request, 'add_product.html', {'error': 'complete all fields'})


def product_list(request):
    if request.method == 'GET':
        # p_list = []
        # for p in Product.objects.all():
        #     p_list.append(
        #         {
        #             'name': p.name,
        #             'quantity': p.quantity
        #         }
        #     )
        return render(request, 'product_list.html', {'p_list': Product.objects.all()})


def product_info(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_info.html', {'product': product})


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        pk = request.POST.get('pk')
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, status='open')
        product = get_object_or_404(Product, pk=pk)
        CartItem.objects.get_or_create(products=product, cart=cart, quantity=quantity)
    return HttpResponseRedirect(reverse('cart'))


def cart(request):
    user = request.user
    cart_obj = user.carts.filter(status='open')
    if cart_obj:
        return render(request, 'cart.html', {'cart': cart_obj[0].items.all()})
    else:
        return render(request, 'cart.html', {'error': 'You have any cart.'})
