import logging
from django.shortcuts import render, redirect
from .utils import get_countries, filter_countries, get_country_id, get_cities, get_airports, get_city_depp
import requests
from django.conf import settings
from datetime import datetime, timedelta
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Booking
import random

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def questions(request):
    if request.method == 'POST':
        continent = request.POST.get('continent')
        weather = request.POST.getlist('weather')
        many_cities = request.POST.get('many_cities')
        departure_date = request.POST.get('departureDate')
        return_date = request.POST.get('returnDate')
        departure_city = request.POST.get('departureCity')
        request.session['continent'] = continent
        request.session['weather'] = weather
        request.session['many_cities'] = many_cities
        request.session['departure_date'] = departure_date
        request.session['return_date'] = return_date
        request.session['departure_city'] = departure_city
        if not get_city_depp(departure_city):
            return render(request, 'questions.html', {'error': 'Please enter a valid departure city.'})
        if not weather:
            return render(request, 'questions.html', {'error_message': 'Please select at least one weather type.'})
        return redirect('results')
    else:
        return render(request, 'questions.html')


def results(request):
    continent = request.session.get('continent')
    weather = request.session.get('weather')
    many_cities = request.session.get('many_cities')
    url = 'https://restcountries.com/v3.1/region/'
    countries = get_countries(url, continent)

    filtered = filter_countries(countries, weather)
    names = [country['name']['common'] for country in filtered]
    countries_id = get_country_id(names)
    filtered = get_cities(countries_id, many_cities)

    return render(request, 'results.html', {'continent': continent, 'data_continents': filtered})


def flights(request, country_name, city_name):
    if request.method == 'POST':
        departure_date = request.POST.get('departureDate')
        return_date = request.POST.get('returnDate')
        departure_city = request.POST.get('departureCity')
        request.session['departure_date'] = departure_date
        request.session['return_date'] = return_date
        request.session['departure_city'] = departure_city
    else:
        departure_date = request.session.get('departure_date')
        return_date = request.session.get('return_date')
        departure_city = request.session.get('departure_city')

    api_key = settings.AVIATIONSTACK_API_KEY

    try:
        airports_depp = get_city_depp(departure_city)
        # Fetch country information
        if country_name == 'United States':
            country_data = {
                'country_name': 'United States',
                'country_iso2': 'US'
            }
            airports_arr = get_airports(country_data['country_iso2'], city_name)
        else:
            country_url = 'http://api.aviationstack.com/v1/countries'
            country_params = {
                'access_key': api_key,
                'limit': 1,
                'search': country_name
            }
            country_response = requests.get(country_url, params=country_params)
            country_response.raise_for_status()
            country_data_list = country_response.json().get('data', [])
            if not country_data_list:
                return render(request, 'flights.html', {
                    'error_message': 'No country information found.'
                })
            country_data = country_data_list[0]

            airports_arr = get_airports(country_data['country_iso2'], city_name)

        # Fetch flight information
        flight_url = 'http://api.aviationstack.com/v1/flights'
        flight_params = {
            'access_key': api_key,
            'dep_iata': airports_depp[0]['iata'],
            'arr_iata': airports_arr[0]['iata'],
            'flight_status': 'scheduled',
            'limit': 5,
        }
        flight_response = requests.get(flight_url, params=flight_params)
        flight_response.raise_for_status()
        flights_data = flight_response.json().get('data', [])

        for flight in flights_data:
            flight['price'] = random.randint(200, 501)

    except requests.RequestException as e:
        logger.error(f"Error fetching data from API: {e}")
        return render(request, 'flights.html', {
            'error_message': 'There was an error retrieving flight data. Please try again later.'
        })

    request.session['flights_data'] = flights_data
    return render(request, 'flights.html', {
        'country_name': country_data['country_name'],
        'city_name': city_name,
        'departure_country': country_data,
        'departure_city': city_name,
        'departure_date': departure_date,
        'flights': flights_data,
        'arrival_iata': airports_arr[0]['iata']
    })


def select_flight(request):
    if request.method == 'POST':
        flight_number = request.POST.get('flight_number')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        departure_airport = request.POST.get('departure_airport')
        arrival_airport = request.POST.get('arrival_airport')
        arrival_country_name = request.POST.get('arrival_country_name')
        arrival_city_name = request.POST.get('arrival_city_name')

        # Store selected flight details in session
        request.session['selected_flight'] = {
            'flight_number': flight_number,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'departure_airport': departure_airport,
            'arrival_airport': arrival_airport
        }

        # Set arrival country and city names in session
        request.session['arrival_country_name'] = arrival_country_name
        request.session['arrival_city_name'] = arrival_city_name

        # Redirect to the return flights selection page
        if arrival_country_name and arrival_city_name:
            return redirect('flights', country_name=arrival_country_name, city_name=arrival_city_name)

    return redirect('index')


@login_required
def book_flight(request):
    if request.method == 'POST':
        flight_number = request.POST.get('flight_number')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        departure_airport = request.POST.get('departure_airport')
        arrival_airport = request.POST.get('arrival_airport')
        price = request.POST.get('price')

        request.session['selected_flight'] = {
            'flight_number': flight_number,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'departure_airport': departure_airport,
            'arrival_airport': arrival_airport,
            'price': price
        }

        booking = Booking.objects.create(
            user=request.user,
            flight_number=flight_number,
            departure_time=departure_time,
            arrival_time=arrival_time,
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            price=price
        )

        return redirect('payment', booking_id=booking.id)

    return redirect('index')


@login_required
def payment(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    select_flight = request.session.get('selected_flight')
    if request.method == 'POST':
        # Simulate payment processing
        booking.paid = True
        booking.save()
        return redirect('booking_confirmation', booking_id=booking.id)

    return render(request, 'payment.html', {'booking': booking, 'flight': select_flight})


@login_required
def booking_confirmation(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})
