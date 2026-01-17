from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('select/', views.select_vehicle, name='select_vehicle'),
    path('my-garage/', views.my_garage, name='my_garage'),
]