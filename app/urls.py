from django.urls import path

from app import views as app_views

urlpatterns = [
    path('add-product/', app_views.add_product, name='add-product'),
    path('product-list/', app_views.product_list, name='product-list'),
    path('product-info/<int:pk>/', app_views.product_info, name='product-info'),
    path('add-to-cart/', app_views.add_to_cart, name='add-to-cart'),
    path('cart', app_views.cart, name='cart'),
    path('remove-from-cart/', app_views.remove_from_cart, name='remove-from-cart'),
    path('category/<str:name>/', app_views.category_view, name='category')
]
