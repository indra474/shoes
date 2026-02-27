from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('products/', views.products, name='products'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/<str:key>/<str:action>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout_all, name='checkout_all'),
    path('remove/<str:key>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]