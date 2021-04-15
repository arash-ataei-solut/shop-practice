from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, Http404
from django.urls import reverse

from app.models import Product, Cart, CartItem, Category


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
        q = request.GET.get('q')
        # p_list = []
        # for p in Product.objects.all():
        #     p_list.append(
        #         {
        #             'name': p.name,
        #             'quantity': p.quantity
        #         }
        #     )
        p_list = Product.objects.all()
        if q:
            p_list = p_list.filter(name__contains=q)

        cat_list = Category.objects.filter(child__isnull=True)
        return render(request, 'product_list.html', {'p_list': p_list, 'cat_list': cat_list})


def product_info(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_info.html', {'product': product})


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity') or '0'
        pk = request.POST.get('pk')
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, status='open')
        product = get_object_or_404(Product, pk=pk)
        cart_item, created2 = CartItem.objects.get_or_create(products=product, cart=cart)
        cart_item.quantity += int(quantity)
        cart_item.save()
    return HttpResponseRedirect(reverse('cart'))


def cart(request):
    user = request.user
    cart_obj = user.carts.filter(status='open')
    if cart_obj:
        return render(request, 'cart.html', {'cart_items': cart_obj[0].items.all()})
    else:
        return render(request, 'cart.html', {'error': 'You have any cart.'})


def remove_from_cart(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
        return HttpResponseRedirect(reverse('cart'))


def category_view(request, name):
    if request.method == 'GET':
        category = get_object_or_404(Category, name=name)
        if category.child:
            raise Http404()
        return render(request, 'category.html', {'p_list': category.product_set.all()})

