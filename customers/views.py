# customers/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Customer, Address, CustomerVehicle
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # ✅ CREATE CUSTOMER HERE
            Customer.objects.create(
                user=user,
                phone='',           # optional
                email=user.email,   # from form
                membership='R'      # default
            )

            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('customers:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'customers/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to profile or next page
            next_url = request.GET.get('next')
            return redirect(next_url) if next_url else redirect('customers:profile')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'customers/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('customers:login')

@login_required
def profile(request):
    customer = request.user.customer
    addresses = customer.addresses.all()
    vehicles = customer.vehicles.select_related('vehicle__model__make').all()

    context = {
        'customer': customer,
        'addresses': addresses,
        'vehicles': vehicles,
    }
    return render(request, 'customers/profile.html', context)