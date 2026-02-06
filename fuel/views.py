import requests
from fuel.utils import best_fuel_stops
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

@api_view(['GET'])
def fuel_price_list(request):
    try:
        # Fetch live fuel prices from internal API
        response = requests.get("http://127.0.0.1:8000/api/fuel-prices/")
        fuel_data = response.json().get("fuel_prices", [])
    except Exception as e:
        return Response({"error": f"Failed to fetch fuel prices: {str(e)}"}, status=500)

    # --- Filters ---
    state = request.GET.get('state')
    city = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if state:
        fuel_data = [row for row in fuel_data if row.get('State') and row['State'].lower() == state.lower()]
    if city:
        fuel_data = [row for row in fuel_data if row.get('City') and row['City'].lower() == city.lower()]
    if min_price:
        fuel_data = [row for row in fuel_data if row.get('Retail Price') and float(row['Retail Price']) >= float(min_price)]
    if max_price:
        fuel_data = [row for row in fuel_data if row.get('Retail Price') and float(row['Retail Price']) <= float(max_price)]

    # --- Sort ---
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        fuel_data.sort(key=lambda x: float(x.get('Retail Price', 0)))
    elif sort == 'price_desc':
        fuel_data.sort(key=lambda x: float(x.get('Retail Price', 0)), reverse=True)

    # --- Pagination ---
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(fuel_data, request)
    
    return paginator.get_paginated_response(result_page)