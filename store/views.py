from django.shortcuts import render


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def customer_home(request):
    print(request.user)
    print('trying to access customer home')
    return render(request, 'customer_home.html', {'user': request.user})

@login_required
def dealer_home(request):
    return render(request, 'dealer_home.html', {'user': request.user})

@login_required
def admin_home(request):
    return render(request, 'admin_home.html', {'user': request.user})


def welcome(request):
    return render(request, 'welcome.html')
    

    
