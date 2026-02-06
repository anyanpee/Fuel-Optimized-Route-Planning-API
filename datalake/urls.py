from django.urls import path
from . import views

urlpatterns = [
    path('', views.fuel_list, name='fuel_list'),
]