#!/bin/bash
echo "=== Fixing ALL image URLs with absolute paths ==="

# Backup
cp README.md README.md.backup

# List of all images with their alt text
declare -A images=(
    ["django_installed_successfully.png"]="Django Installation"
    ["Django_server_running_on_browser.png"]="Django Server Running"
    ["django_secret_key_for_api_created.png"]="Django Secret Key"
    ["migration_for_datalake_success_on_terminal.png"]="Migration Success"
    ["fuel_data_imported_success_on_terminal.png"]="Fuel Data Import"
    ["Geopy_installled_successfully.png"]="Geopy Installation"
    ["open_route_service_dashboard.png"]="OpenRouteService Dashboard"
    ["Api_handling_missing_values_and_filtering_by_states_and_address.png"]="API Data Handling"
    ["accessing_fuel_Api_on_browser.png"]="Fuel API Access"
    ["fuel_price.csv_served_by_django_api_on_browser.png"]="Fuel CSV API"
    ["api_response_with_200_successful_response.png"]="API Response Success"
    ["fuel_price_calculation_success_response_for_state_with_cheapest_fuel.png"]="Fuel Calculation Success"
    ["api_postman_response_for_calculating_routes_distance_and_fuel_cost.png"]="Route Calculation Response"
)

# Base URL for your GitHub repository
BASE_URL="https://github.com/anyanpee/Fuel-Optimized-Route-Planning-API/raw/main/README/images"

# Process the README.md file
while IFS= read -r line; do
    # Check if this line has an image reference
    for img in "${!images[@]}"; do
        if [[ "$line" == *"$img"* ]]; then
            # Replace with absolute URL
            line="![${images[$img]}]($BASE_URL/$img)"
            break
        fi
    done
    echo "$line"
done < README.md.backup > README.md.new

# Replace the file
mv README.md.new README.md

echo "✅ All image URLs updated to absolute GitHub URLs"
echo ""
echo "Example:"
echo "BEFORE: ![Alt](README/images/filename.png)"
echo "AFTER:  ![Alt]($BASE_URL/filename.png)"
