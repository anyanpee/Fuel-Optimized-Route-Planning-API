import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from datalake.models import FuelPrice

class Command(BaseCommand):
    help = 'Imports fuel price data from CSV file into the database'

    def handle(self, *args, **kwargs):
        with open('datalake/fuel_prices.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if price exists before trying to convert
                if row['Retail Price']:
                    try:
                        FuelPrice.objects.create(
                            station_name = row['Truckstop Name'],
                            fuel_type = 'Diesel',
                            price = float(row['Retail Price']),
                            date = datetime.today().date()
                        )
                    except Exception as e:
                        print(f"Skipping row due to error: {e}")
        self.stdout.write(self.style.SUCCESS('Fuel data imported successfully.'))