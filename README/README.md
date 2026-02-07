Fuel-Optimized Route Planning API
📋 Project Overview

A Django-based REST API that calculates optimal driving routes between US cities with intelligent fuel stop recommendations. The system considers vehicle range (500 miles), fuel efficiency (10 MPG), and real-time fuel prices to minimize travel costs.
🎯 Features

    Route Calculation: Get driving routes between any two US locations

    Fuel Optimization: Smart fuel stop placement based on 500-mile vehicle range

    Cost Calculation: Total fuel cost estimation at 10 MPG efficiency

    CSV Integration: Uses provided fuel price data for cost optimization

    Fast API: Single external API call to OpenRouteService for efficiency

🛠️ Step-by-Step Implementation Guide
Step 1: Environment Setup

*Prerequisites: Python 3.11+, pip, virtual environment*
bash

# Create project directory
mkdir spotter_Api
cd spotter_Api

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Verify Python version
python --version

Step 2: Django Installation and Project Setup
bash

# Install Django and required packages
pip install django
pip install djangorestframework
pip install requests
pip install python-dotenv
pip install geopy

# Verify Django installation
python -m django --version

<!-- SCREENSHOT: Django Installation Success -->
![](<django installed successfully Screenshot .png>)

# Create Django project
django-admin startproject spotter_api .

# Create apps for different functionalities
python manage.py startapp routes
python manage.py startapp fuel
python manage.py startapp datalake

<!-- SCREENSHOT: Django Server Running -->
![](<Django server running on browser Screenshot .png>)

Step 3: Project Configuration
bash

# Create .env file for environment variables
echo "ORS_API_KEY=your_openrouteservice_key_here" > .env
echo "SECRET_KEY=your_django_secret_key_here" >> .env

# Generate Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

<!-- SCREENSHOT: Django Secret Key Generated -->
![](<django secret key for api created  Screenshot .png>)

Update settings.py:
python

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ORS_API_KEY = os.getenv('ORS_API_KEY')

INSTALLED_APPS = [
    'rest_framework',
    'routes',
    'fuel',
    'datalake',
]

Step 4: Data Setup
bash

# Create data directory for CSV files
mkdir data

# Place the fuel price CSV in data directory
# Your file should be at: data/fuel-prices-for-be-assessment.csv

# Create models for datalake app

In datalake/models.py:
python

from django.db import models

class FuelPrice(models.Model):
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=100)
    retail_price = models.DecimalField(max_digits=5, decimal_places=3)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    class Meta:
        db_table = 'fuel_prices'

<!-- SCREENSHOT: Migration Success -->
![](<migration for datalake success on terminal Screenshot .png>)

# Run migrations
python manage.py makemigrations
python manage.py migrate

<!-- SCREENSHOT: Fuel Data Import -->
![](<fuel data imported success on termnal Screenshot .png>)

Step 5: API Integration Setup
bash

# Install geopy for distance calculations
pip install geopy

<!-- SCREENSHOT: Geopy Installation -->
![](<Geopy installled successfully Screenshot.png>)

# Sign up for OpenRouteService API key
# Visit: https://openrouteservice.org/dev/#/signup
# Add your API key to .env file

<!-- SCREENSHOT: OpenRouteService Dashboard -->
![](<open route service dashboard Screenshot .png>)

Create routes/utils.py:
python

import os
import csv
import math
from geopy.distance import geodesic

def load_fuel_data():
    """Load and parse fuel price CSV"""
    csv_path = os.path.join('data', 'fuel-prices-for-be-assessment.csv')
    # Implementation details...

Create routes/services.py:
python

import requests
from django.conf import settings

def get_route_geometry(start_coords, end_coords):
    """Call OpenRouteService API"""
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {'Authorization': settings.ORS_API_KEY}
    # Implementation details...

<!-- SCREENSHOT: API Data Handling -->
![](<Api handling missing values and filtering by states and address Screenshot .png>)

Step 7: Implement API Views

Create routes/views.py:
python

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import get_route_geometry
from .utils import calculate_fuel_stops

@api_view(['POST'])
def calculate_route(request):
    """Main API endpoint for route calculation"""
    # Implementation details...

Update routes/urls.py:
python

from django.urls import path
from .views import calculate_route

urlpatterns = [
    path('api/calculate-route/', calculate_route, name='calculate_route'),
]

<!-- SCREENSHOT: Fuel API Access -->
![](<accessing fuel Api on browser Screenshot.png>)

Step 8: Fuel Price API Endpoint

Create fuel/views.py:
python

from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import os

class FuelPriceAPI(APIView):
    def get(self, request):
        csv_path = os.path.join('data', 'fuel-prices-for-be-assessment.csv')
        df = pd.read_csv(csv_path)
        return Response(df.to_dict('records'))

<!-- SCREENSHOT: Fuel CSV API -->
![](<fuel price.csv served by django api on browser Screenshot .png>)

Step 9: Testing with Postman
bash

# Start Django development server
python manage.py runserver

Postman Configuration:

    Method: POST

    URL: http://localhost:8000/api/calculate-route/

    Headers: Content-Type: application/json

    Body (JSON):

json

{
    "start": [-95.3698, 29.7604],
    "end": [-96.7969, 32.7767]
}

<!-- SCREENSHOT: API Response Success -->
![](<api response with 200 successful response Screenshot.png>)

Step 10: Response Validation

Expected API Response Structure:
json

{
    "status": "success",
    "route_distance_miles": 238.88,
    "total_fuel_cost": 76.45,
    "map_route": [...],
    "recommended_stops": [...],
    "debug_info": {...}
}

<!-- SCREENSHOT: Fuel Calculation Success -->
![](<fuel_price_calculation_success_response for state with cheapest fuel Screenshot .png>)

<!-- SCREENSHOT: Route Calculation Response -->
![](<api postman response for calculating routes distance and fuel cost Screenshot .png>)

![](<successfull post in postman for calculating distance, gallon of fuel and state map Screenshot .png>)

Step 11: Error Handling Implementation

Update your views with comprehensive error handling:
python

try:
    # API logic
    result = calculate_optimal_route(start, end)
    return Response(result, status=200)
except Exception as e:
    return Response({
        "error": str(e),
        "status": "error"
    }, status=500)

Step 12: Performance Optimization
python

# Implement caching for fuel data
from django.core.cache import cache

def get_cached_fuel_data():
    data = cache.get('fuel_data')
    if not data:
        data = load_fuel_data()
        cache.set('fuel_data', data, 3600)  # Cache for 1 hour
    return data

Step 13: API Documentation

Create API_DOCUMENTATION.md:
markdown

## API Endpoints

### 1. Calculate Route
**POST** `/api/calculate-route/`

**Request Body:**
```json
{
    "start": [longitude, latitude],
    "end": [longitude, latitude]
}

2. Get Fuel Prices

GET /api/fuel-prices/
text


### **Step 14: Deployment Preparation**
```bash
# Install production requirements
pip install gunicorn
pip install psycopg2-binary

# Create requirements.txt
pip freeze > requirements.txt

# Create Procfile for deployment
echo "web: gunicorn spotter_api.wsgi --log-file -" > Procfile

Step 15: Testing Scenarios

Test different scenarios:

    Short route (<500 miles)

    Long route (>500 miles)

    Multiple fuel stops required

    Edge cases (missing data, invalid coordinates)

bash

# Run Django tests
python manage.py test routes.tests

📁 Project Structure
text

spotter_Api/
├── README.md                    # This documentation file
├── data/
│   └── fuel-prices-for-be-assessment.csv
├── routes/
│   ├── views.py          # API endpoints
│   ├── services.py       # External API calls
│   └── utils.py          # Calculation utilities
├── fuel/                 # Fuel price API app
├── datalake/            # Data models and storage
├── manage.py
├── requirements.txt
└── .env

🔧 Environment Variables
env

ORS_API_KEY=your_openrouteservice_api_key
SECRET_KEY=your_django_secret_key
DEBUG=True

🚀 Quick Start

Clone and setup:
bash

git clone <repository-url>
cd spotter_Api
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

Configure environment:
bash

cp .env.example .env
# Edit .env with your API keys

Run migrations:
bash

python manage.py migrate

Start server:
bash

python manage.py runserver

Test API:
bash

curl -X POST http://localhost:8000/api/calculate-route/ \
  -H "Content-Type: application/json" \
  -d '{"start":[-95.3698,29.7604],"end":[-96.7969,32.7767]}'

📊 Algorithm Overview

    Route Calculation: Single call to OpenRouteService API

    Distance Analysis: Calculate total route distance

    Fuel Stop Planning:

        If distance < 500 miles: No stops needed

        If distance > 500 miles: Place stops every ~450 miles

    Cost Optimization: Select cheapest fuel stations along route

    Total Cost: Calculate based on 10 MPG efficiency