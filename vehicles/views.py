from django.shortcuts import render, redirect
from .models import Make, Model, Vehicle

def select_vehicle(request):
    """Vehicle selection wizard"""
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        request.session['selected_vehicle_id'] = vehicle_id
        return redirect('products:product_list')
    
    makes = Make.objects.all()
    
    # AJAX data for dynamic dropdowns
    make_id = request.GET.get('make')
    model_id = request.GET.get('model')
    
    models = Model.objects.filter(make_id=make_id) if make_id else []
    vehicles = Vehicle.objects.filter(model_id=model_id) if model_id else []
    
    context = {
        'makes': makes,
        'models': models,
        'vehicles': vehicles,
    }
    return render(request, 'vehicles/select_vehicle.html', context)

def my_garage(request):
    """Customer's saved vehicles"""
    if not request.user.is_authenticated:
        return redirect('customers:login')
    
    customer_vehicles = request.user.customer.vehicles.all()
    
    context = {
        'customer_vehicles': customer_vehicles,
    }
    return render(request, 'vehicles/my_garage.html', context)