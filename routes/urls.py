print("[+] routes.urls.py loaded")

from django.urls import path
from .views import calculate_route  # ✅ Add this to import your route view
urlpatterns = [
    path('calculate-route/', calculate_route),
    path("calculate-route/", calculate_route, name="calculate-route"),
]  