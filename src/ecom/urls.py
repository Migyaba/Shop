from django.urls import path
from .views import product_detail, index, add_to_cart, cart_total

urlpatterns = [
    path('', index, name='index'),
    path('produit/<int:pk>/', product_detail, name='product_detail'),
    path('ajouter-au-panier/', add_to_cart, name='add_to_cart'),
    path('cart-total/', cart_total, name='cart_total'),
]