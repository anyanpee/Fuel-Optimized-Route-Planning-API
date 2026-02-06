from django.db import models

class FuelPrice(models.Model):
    station_name = models.CharField(max_length=255)
    fuel_type = models.CharField(max_length=50, default='Diesel')  # hardcoded value
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)  # use today's date