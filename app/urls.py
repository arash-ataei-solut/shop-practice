from django.urls import path

from app.views import add_product, product_list, product_info, add_to_cart, cart

urlpatterns = [
    path('add-product/', add_product, name='add-product'),
    path('product-list/', product_list, name='product-list'),
    path('product-info/<int:pk>/', product_info, name='product-info'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart', cart, name='cart')
]
