from django.shortcuts import render
from .models import FuelPrice

def fuel_list(request):
    fuels = FuelPrice.objects.all()
    return render(request, 'fuel_list.html', {'fuels': fuels})
