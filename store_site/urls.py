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
from store.views import welcome, customer_home, admin_home, list_categories, add_category, delete_category, list_products, add_product, update_product, delete_product 
from accounts.views import login_view, user_signup, dealer_signup
from django.conf import settings
from django.conf.urls.static import static
from store.views import customer_home, add_to_cart, remove_from_cart

urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('', welcome, name=''),
    path('login/', login_view, name='login'),
    path('user/signup/', user_signup, name='user_signup'),
    path('dealer/signup/', dealer_signup, name='dealer_signup'),

    # Customer URLs
    path('home/customer/', customer_home, name='customer_home'),
    path('home/customer/cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('home/customer/cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),

      # Dealer category management URLs
    path('categories/', list_categories, name='list_categories'),
    path('categories/add/', add_category, name='add_category'),
    path('categories/delete/<int:id>/', delete_category, name='delete_category'),
    path('categories/<int:id>/products/', list_products, name='list_products'),
    path('categories/<int:id>/products/add/', add_product, name='add_product'),
    path('products/<int:product_id>/update/',  update_product, name='update_product'),
    path('products/<int:product_id>/delete/', delete_product, name='delete_product'),

]