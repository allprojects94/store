from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignupForm, DealerSignupForm



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Redirect based on role
            if user.role == 'customer':
                return redirect('customer_home')  # Change to your customer home view
            elif user.role == 'dealer':
                return redirect('list_categories')    # Change to your dealer home view
            elif user.role == 'admin':
                return redirect('')    # Change to your admin home view
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User account created successfully!")
            return redirect('login')  # Redirect to login page
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form, 'user_type': 'User'})

def dealer_signup(request):
    if request.method == 'POST':
        form = DealerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Dealer account created successfully!")
            return redirect('login')  # Redirect to login page
    else:
        form = DealerSignupForm()
    return render(request, 'signup.html', {'form': form, 'user_type': 'Dealer'})
