import json
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fuel.utils import best_fuel_stops

@csrf_exempt
def calculate_route(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Only POST requests allowed"},
            status=405
        )
    
    print("\n" + "="*60)
    print("🚀 CALCULATE_ROUTE CALLED")
    
    try:
        # 1. Parse request
        try:
            body = request.body.decode("utf-8")
            data = json.loads(body)
            print(f"✅ Request body parsed: {data}")
        except json.JSONDecodeError as e:
            return JsonResponse(
                {"status": "error", "message": f"Invalid JSON: {str(e)}"},
                status=400
            )
        
        start = data.get("start")
        end = data.get("end")
        
        if not start or not end:
            return JsonResponse(
                {"status": "error", "message": "Start and end coordinates are required"},
                status=400
            )
        
        print(f"📍 Start: {start}, End: {end}")
        
        # 2. Get ORS API key
        ors_api_key = os.getenv("ORS_API_KEY")
        print(f"🔑 ORS_API_KEY loaded: {'YES' if ors_api_key else 'NO'}")
        
        if not ors_api_key:
            return JsonResponse(
                {
                    "status": "error", 
                    "message": "ORS_API_KEY not found. Check your .env file.",
                    "debug": "Set ORS_API_KEY=your_key_here in .env file"
                },
                status=500
            )
        
        # 3. Call OpenRouteService - TRY WITH QUERY PARAM FOR FORMAT
        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {
            "Authorization": ors_api_key.strip(),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Payload without format
        payload = {
            "coordinates": [start, end]
        }
        
        # Try with query parameter for format
        params = {"format": "geojson"}
        
        print(f"📡 Calling ORS: {url}")
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")
        print(f"🔧 Params: {params}")
        
        try:
            response = requests.post(
                url, 
                headers=headers, 
                json=payload, 
                params=params,  # ✅ Add format as query parameter
                timeout=30
            )
            print(f"📊 ORS Response Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ ORS Error Response: {response.text[:200]}")
                return JsonResponse(
                    {
                        "status": "error",
                        "message": f"ORS API returned error {response.status_code}",
                        "ors_status": response.status_code,
                        "ors_error": response.text[:500] if response.text else "No error message"
                    },
                    status=500
                )
            
            route_data = response.json()
            print("✅ ORS Response received and parsed")
            print(f"📄 Response keys: {list(route_data.keys())}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ RequestException: {str(e)}")
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Network error: {str(e)}",
                    "debug": "Check internet connection or ORS API availability"
                },
                status=500
            )
        
        # 4. Handle BOTH response formats
        route_geometry = []
        distance_meters = 0
        
        # Format 1: GeoJSON (with "features")
        if "features" in route_data:
            print("✅ Detected GeoJSON format (features)")
            features = route_data.get("features", [])
            if features:
                feature = features[0]
                geometry = feature.get("geometry", {})
                
                if isinstance(geometry, dict) and "coordinates" in geometry:
                    route_geometry = geometry["coordinates"]
                
                properties = feature.get("properties", {})
                if "summary" in properties:
                    summary = properties["summary"]
                    distance_meters = summary.get("distance", 0)
                elif "segments" in properties and properties["segments"]:
                    segments = properties["segments"]
                    distance_meters = sum(seg.get("distance", 0) for seg in segments)
        
        # Format 2: Default format (with "routes")
        elif "routes" in route_data:
            print("✅ Detected default format (routes)")
            routes = route_data.get("routes", [])
            if routes:
                route = routes[0]
                geometry = route.get("geometry", {})
                
                if isinstance(geometry, dict) and "coordinates" in geometry:
                    route_geometry = geometry["coordinates"]
                elif isinstance(geometry, str):
                    # Encoded polyline - decode it
                    print("⚠️ Got encoded polyline, attempting to decode...")
                    try:
                        import polyline
                        # polyline.decode returns [(lat, lng), ...]
                        decoded = polyline.decode(geometry)
                        # Convert to GeoJSON format [(lng, lat), ...]
                        route_geometry = [[lng, lat] for lat, lng in decoded]
                    except ImportError:
                        print("❌ polyline module not installed. Install: pip install polyline")
                        route_geometry = []
                
                summary = route.get("summary", {})
                distance_meters = summary.get("distance", 0)
        
        else:
            print(f"❌ Unknown response format. Keys: {list(route_data.keys())}")
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Unexpected ORS response format",
                    "ors_response_keys": list(route_data.keys()),
                    "sample_response": json.dumps(route_data)[:500]
                },
                status=500
            )
        
        if not route_geometry:
            print("❌ No route geometry extracted")
            return JsonResponse(
                {"status": "error", "message": "Could not extract route geometry"},
                status=500
            )
        
        print(f"✅ Geometry extracted: {len(route_geometry)} points")
        if route_geometry:
            print(f"   First point: {route_geometry[0]}")
            print(f"   Last point: {route_geometry[-1]}")
        
        print(f"📏 Distance: {distance_meters} meters")
        
        # 5. Distance & fuel math
        distance_miles = round(distance_meters * 0.000621371, 2)
        gallons_needed = round(distance_miles / 10, 2)
        
        print(f"📏 Distance: {distance_miles} miles")
        print(f"⛽ Gallons needed: {gallons_needed}")
        
        # 6. Fuel stops
        recommended_stops = best_fuel_stops(route_geometry)
        print(f"🛑 Fuel stops found: {len(recommended_stops)}")
        
        if recommended_stops:
            avg_price = sum(stop["fuel_price"] for stop in recommended_stops) / len(recommended_stops)
            avg_price = round(avg_price, 2)
            print(f"💰 Fuel stops: {recommended_stops}")
        else:
            avg_price = 0
            print("⚠️ No fuel stops found")
        
        total_fuel_cost = round(avg_price * gallons_needed, 2)
        
        print(f"💰 Avg fuel price: ${avg_price}")
        print(f"💵 Total fuel cost: ${total_fuel_cost}")
        print("="*60 + "\n")
        
        # 7. Final response
        return JsonResponse(
            {
                "status": "success",
                "route_distance_miles": distance_miles,
                "total_fuel_cost": total_fuel_cost,
                "map_route": route_geometry[:10] if route_geometry else [],  # First 10 points only
                "recommended_stops": recommended_stops,
                "debug_info": {
                    "geometry_points": len(route_geometry),
                    "avg_fuel_price": avg_price,
                    "gallons_needed": gallons_needed,
                    "distance_meters": distance_meters,
                    "format_detected": "geojson" if "features" in route_data else "default"
                }
            },
            status=200
        )
        
    except Exception as e:
        print(f"💥 Unhandled exception: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return JsonResponse(
            {
                "status": "error",
                "message": f"Internal server error: {str(e)}",
                "debug": "Check server logs for details"
            },
            status=500
        )