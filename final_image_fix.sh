#!/bin/bash
echo "=== Applying FINAL image fix ==="

# Base URL for raw GitHub content
BASE_URL="https://raw.githubusercontent.com/anyanpee/Fuel-Optimized-Route-Planning-API/main/README/images"

# Update README.md
sed -i "
s|!\[Django Installation\](README/images/django_installed_successfully.png)|![Django Installation]($BASE_URL/django_installed_successfully.png)|g
s|!\[Django Server Running\](README/images/Django_server_running_on_browser.png)|![Django Server Running]($BASE_URL/Django_server_running_on_browser.png)|g
s|!\[Django Secret Key\](README/images/django_secret_key_for_api_created.png)|![Django Secret Key]($BASE_URL/django_secret_key_for_api_created.png)|g
s|!\[Migration Success\](README/images/migration_for_datalake_success_on_terminal.png)|![Migration Success]($BASE_URL/migration_for_datalake_success_on_terminal.png)|g
s|!\[Fuel Data Import\](README/images/fuel_data_imported_success_on_terminal.png)|![Fuel Data Import]($BASE_URL/fuel_data_imported_success_on_terminal.png)|g
s|!\[Geopy Installation\](README/images/Geopy_installled_successfully.png)|![Geopy Installation]($BASE_URL/Geopy_installled_successfully.png)|g
s|!\[OpenRouteService Dashboard\](README/images/open_route_service_dashboard.png)|![OpenRouteService Dashboard]($BASE_URL/open_route_service_dashboard.png)|g
s|!\[API Data Handling\](README/images/Api_handling_missing_values_and_filtering_by_states_and_address.png)|![API Data Handling]($BASE_URL/Api_handling_missing_values_and_filtering_by_states_and_address.png)|g
s|!\[Fuel API Access\](README/images/accessing_fuel_Api_on_browser.png)|![Fuel API Access]($BASE_URL/accessing_fuel_Api_on_browser.png)|g
s|!\[Fuel CSV API\](README/images/fuel_price.csv_served_by_django_api_on_browser.png)|![Fuel CSV API]($BASE_URL/fuel_price.csv_served_by_django_api_on_browser.png)|g
s|!\[API Response Success\](README/images/api_response_with_200_successful_response.png)|![API Response Success]($BASE_URL/api_response_with_200_successful_response.png)|g
s|!\[Fuel Calculation Success\](README/images/fuel_price_calculation_success_response_for_state_with_cheapest_fuel.png)|![Fuel Calculation Success]($BASE_URL/fuel_price_calculation_success_response_for_state_with_cheapest_fuel.png)|g
s|!\[Route Calculation Response\](README/images/api_postman_response_for_calculating_routes_distance_and_fuel_cost.png)|![Route Calculation Response]($BASE_URL/api_postman_response_for_calculating_routes_distance_and_fuel_cost.png)|g
" README.md

echo "✅ Updated all image URLs to use raw.githubusercontent.com"
echo ""
echo "Test URLs:"
echo "1. $BASE_URL/django_installed_successfully.png"
echo "2. $BASE_URL/api_response_with_200_successful_response.png"
