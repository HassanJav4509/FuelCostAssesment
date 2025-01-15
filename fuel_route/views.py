import requests
from django.http import JsonResponse
from django.conf import settings
from .models import FuelPrice
from geopy.distance import geodesic
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('HERE_API_KEY')

def get_coordinates(location):
    geocode_url = "https://geocode.search.hereapi.com/v1/geocode"
    response = requests.get(geocode_url, params={'q': location, 'apiKey': API_KEY})

    if response.status_code == 200:
        data = response.json()
        if data.get('items'):
            position = data['items'][0]['position']
            return f"{position['lat']},{position['lng']}"
        else:
            return None
    else:
        return None


def calculate_fuel_stops(route, mpg=10, max_range=500):
    stops = []
    total_fuel_cost = 0

    departure = route['sections'][0]['departure']['place']['location']
    arrival = route['sections'][0]['arrival']['place']['location']
    total_distance = geodesic(
        (departure['lat'], departure['lng']),
        (arrival['lat'], arrival['lng'])
    ).miles

    remaining_distance = total_distance
    while remaining_distance > max_range:
        midpoint_lat = (departure['lat'] + arrival['lat']) / 2
        midpoint_lng = (departure['lng'] + arrival['lng']) / 2

        nearest_stop = FuelPrice.objects.order_by('retail_price').first()

        if nearest_stop:
            stops.append({
                'location': f"{nearest_stop.truckstop_name}, {nearest_stop.city}, {nearest_stop.state}",
                'price_per_gallon': nearest_stop.retail_price
            })
            fuel_needed = max_range / mpg
            total_fuel_cost += fuel_needed * nearest_stop.retail_price

        remaining_distance -= max_range

    if remaining_distance > 0:
        nearest_stop = FuelPrice.objects.order_by('retail_price').first()
        if nearest_stop:
            stops.append({
                'location': f"{nearest_stop.truckstop_name}, {nearest_stop.city}, {nearest_stop.state}",
                'price_per_gallon': nearest_stop.retail_price
            })
            fuel_needed = remaining_distance / mpg
            total_fuel_cost += fuel_needed * nearest_stop.retail_price

    return {
        'stops': stops,
        'total_fuel_cost': total_fuel_cost
    }


def get_route(request):
    start = request.GET.get('start')
    finish = request.GET.get('finish')

    if not start or not finish:
        return JsonResponse({'error': 'Start and finish locations are required'}, status=400)

    start_coordinates = get_coordinates(start)
    finish_coordinates = get_coordinates(finish)

    if not start_coordinates or not finish_coordinates:
        return JsonResponse({'error': 'Failed to geocode one or both locations'}, status=400)

    api_url = "https://router.hereapi.com/v8/routes"
    params = {
        'origin': start_coordinates,
        'destination': finish_coordinates,
        'transportMode': 'car',
        'apiKey': API_KEY
    }


    try:
        response = requests.get(api_url, params=params)

        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to fetch route'}, status=500)

        data = response.json()
        if not data.get('routes'):
            return JsonResponse({'error': 'Invalid route data'}, status=400)

        route = data['routes'][0]
        fuel_data = calculate_fuel_stops(route)

        return JsonResponse({
            'route': route,
            'fuel_data': fuel_data
        })

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
