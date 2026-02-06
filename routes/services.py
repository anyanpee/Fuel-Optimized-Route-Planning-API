print("[+] [DEBUG] services.py loaded")  # Confirms the file was loaded.

import requests
from django.conf import settings

def get_route_details(start_coords, end_coords):
    url = 'https://api.openrouteservice.org/v2/directions/driving-car'

    # Convert input to lists in case they are passed as tuples
    if isinstance(start_coords, tuple):
        start_coords = list(start_coords)
    if isinstance(end_coords, tuple):
        end_coords = list(end_coords)

    headers = {
        'Authorization': settings.ORS_API_KEY,
        'Content-Type': 'application/json'
    }

    payload = {
        'coordinates': [start_coords, end_coords]
    }

    try:
        print("[DEBUG] Sending POST request to ORS API...")
        print(f"[DEBUG] Payload: {payload}")
        print(f"[DEBUG] Headers: {headers}")

        response = requests.post(url, json=payload, headers=headers)

        print(f"[DEBUG] Received response with status code: {response.status_code}")
        print(f"[DEBUG] Raw API Response: {response.text}")

        response.raise_for_status()  # Raises error if not 2XX

        data = response.json()

        route = data['features'][0]['properties']['segments'][0]
        geometry = data['features'][0]['geometry']['coordinates']

        return {
            'distance_km': round(route['distance'] / 1000, 2),
            'duration_min': round(route['duration'] / 60, 2),
            'path': geometry
        }

    except requests.RequestException as e:
        print(f"[ERROR] Routing API call failed: {e}")
        return {'error': f'Routing service failed: {str(e)}'}