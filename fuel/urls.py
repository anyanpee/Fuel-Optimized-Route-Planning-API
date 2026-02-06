from django.urls import path
from .views import dummy_view, fuel_price_list

urlpatterns = [
    path('ping/', dummy_view),
    path('fuel-prices/', fuel_price_list),
]
