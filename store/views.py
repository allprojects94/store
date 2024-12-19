from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Category, Product
from accounts.models import CustomUser
from django.http import HttpResponse
from store.models import Cart


# Welcome page
def welcome(request):
    return render(request, 'welcome.html')


# Customer Views
@login_required
def customer_home(request):
    # Get all products and categories joined  
    products = Product.objects.all()
    userCart = Cart.objects.filter(user=request.user)
    
    # Get the number of items in the cart
    cart_count = len(userCart)

    for product in products:
        product.category = Category.objects.get(id=product.category_id)
        product.cart_quantity = 0
        for cart_item in userCart:
            if cart_item.product_id == product.id:
                product.cart_quantity = cart_item.quantity
                break

    return render(request, 'customer/store.html', {'products': products, 'cart_count': cart_count})


@login_required
def customer_cart(request):
    userCart = Cart.objects.filter(user=request.user)
    total = 0
    for cart_item in userCart:
        cart_item.product = Product.objects.get(id=cart_item.product_id)
        cart_item.total = cart_item.product.price * cart_item.quantity
        total += cart_item.total

    return render(request, 'customer/cart.html', {'cart': userCart, 'total': total})


@login_required
def increase_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('customer_cart')


@login_required
def decrease_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        cart_item.quantity -= 1
        if cart_item.quantity == 0:
            cart_item.delete()
        else:
            cart_item.save()

    return redirect('customer_cart')


# Remove a product from the cart
@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        cart_item.delete()

    return redirect('customer_cart')


@login_required
def remove_from_cart_from_home(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        cart_item.delete()

    return redirect('customer_home')


# Add a product to the cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item is None:   
        Cart.objects.create(user=user, product=product, quantity=1)

    return redirect('customer_home')


# Dealer permission check
def dealer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'dealer':
            return view_func(request, *args, **kwargs)
        return redirect('login')  # Redirect unauthorized users
    return wrapper


# View list of categories
@login_required
@dealer_required
def list_categories(request):
    categories = Category.objects.filter(dealer_id=request.user)
    return render(request, 'dealer/list_categories.html', {'categories': categories, 'user': request.user})


# Add a new category
@login_required
@dealer_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        division = request.POST.get('division')
        status = request.POST.get('status') == 'on'  # Checkbox for status
        if name and division:
            Category.objects.create(name=name, division=division, status=status, dealer_id=request.user)
        return redirect('list_categories')
    return render(request, 'dealer/add_category.html', {'user': request.user})


# Delete a category (and all its products)
@login_required
@dealer_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id, dealer_id=request.user)
    category.delete()
    return redirect('list_categories')


# Add a product to a category
@login_required
@dealer_required
def add_product(request, id):
    category = get_object_or_404(Category, id=id, dealer_id=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        color = request.POST.get('color')
        image_url = request.POST.get('image_url')
        price = request.POST.get('price')

        if title and description and quantity.isdigit():
            Product.objects.create(
                title=title,
                description=description,
                quantity=int(quantity),
                color=color,
                image_url=image_url,
                category=category,
                price=price
            )
        return redirect('list_products', id=id)
    return render(request, 'dealer/add_product.html', {'category': category, 'user': request.user})


@login_required
@dealer_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    category = product.category
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        color = request.POST.get('color')
        image_url = request.POST.get('image_url')
        price = request.POST.get('price')

        if title and description and quantity.isdigit():
            product.title = title
            product.description = description
            product.quantity = int(quantity)
            product.color = color
            product.image_url = image_url
            product.price = price
            product.save()

            return redirect('list_products', id=category.id)

    return render(request, 'dealer/update_product.html', {
        'product': product,
        'category': category,
        'user': request.user
    })


# View all products in a category
@login_required
@dealer_required
def list_products(request, id):
    category = get_object_or_404(Category, id=id, dealer_id=request.user)
    products = Product.objects.filter(category=category)
    return render(request, 'dealer/list_products.html', {'products': products, 'category': category})


# Delete a product
@login_required
@dealer_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    id = product.category.id
    product.delete()
    return redirect('list_products', id=id)


# Admin Views
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        return redirect('login')  # Redirect unauthorized users
    return wrapper


@login_required
@admin_required
def admin_home(request):
    users = CustomUser.objects.all()
    return render(request, 'admin/manage.html', {'users': users})


@login_required
@admin_required
def toggle_approve_dealer(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_dealer_approved = not user.is_dealer_approved
    user.save()
    return redirect('admin_home')
