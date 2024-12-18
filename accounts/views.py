from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignupForm, DealerSignupForm
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = CustomUser.objects.get(username=username)
        print(user.password, 'user from login view')
        
        if user is None:
            messages.error(request, 'User does not exist.')
            return render(request, 'login.html')
        elif user.password == password:
            print('password match')
            if user.role == 'customer':
                print('customer role match')
                return redirect('')
            elif user.role == 'dealer':
                return redirect('')
            elif user.role == 'admin':
                return redirect('')
            else:
                messages.error(request, 'Incorrect password.')
                return render(request, 'login.html')
      
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
