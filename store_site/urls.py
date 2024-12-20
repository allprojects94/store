"""
URL configuration for store_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin 
from django.urls import path, include 
from store.views import welcome, about, list_categories, add_category, delete_category, list_products, add_product, update_product, delete_product 
from accounts.views import login_view, user_signup, dealer_signup, logout_view
from django.conf import settings
from store.views import customer_home, customer_cart, add_to_cart, remove_from_cart, increase_quantity, decrease_quantity, remove_from_cart_from_home
from store.views import admin_home, toggle_approve_dealer

urlpatterns = [ 
    # path('admin/', admin.site.urls), 
    path('', welcome, name=''),
    path('about/', about, name='about'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/signup/', user_signup, name='user_signup'),
    path('dealer/signup/', dealer_signup, name='dealer_signup'),

    # Customer URLs
    path('home/customer/', customer_home, name='customer_home'),
    path('home/customer/cart/', customer_cart, name='customer_cart'),
    path('home/customer/cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('home/customer/cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('home/customer/cart/remove_from_home/<int:product_id>/', remove_from_cart_from_home, name='remove_from_cart_from_home'),  # Add
    path('home/customer/cart/increase/<int:product_id>/', increase_quantity, name='increase_quantity'),
    path('home/customer/cart/decrease/<int:product_id>/', decrease_quantity, name='decrease_quantity'),


      # Dealer category management URLs
    path('home/dealer/categories/', list_categories, name='list_categories'),
    path('home/dealer/categories/add/', add_category, name='add_category'),
    path('home/dealer/categories/delete/<int:id>/', delete_category, name='delete_category'),
    path('home/dealer/categories/<int:id>/list-products/', list_products, name='list_products'),
    path('home/dealer/categories/<int:id>/add-products', add_product, name='add_product'),
    path('home/dealer/products/update/<int:product_id>',  update_product, name='update_product'),
    path('home/dealer/products/delete/<int:product_id>/', delete_product, name='delete_product'),


    # Admin user management URLs
    path('home/admin/', admin_home, name='admin_home'),
    path('home/admin/toggle-approve-dealer/<int:user_id>/', toggle_approve_dealer, name='toggle_approve_dealer'),



]