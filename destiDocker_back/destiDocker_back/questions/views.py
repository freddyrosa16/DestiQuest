# views.py
import logging
from django.shortcuts import render, redirect
from .utils import get_countries, filter_countries, get_country_id, get_cities, get_flights
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def questions(request):
    if request.method == 'POST':
        continent = request.POST.get('continent')
        weather = request.POST.getlist('weather')
        population = request.POST.get('population')
        many_cities = request.POST.get('many_cities')
        departure_date = request.POST.get('departureDate')
        return_date = request.POST.get('returnDate')
        departure_city = request.POST.get('departureCity')
        request.session['continent'] = continent
        request.session['weather'] = weather
        request.session['population'] = population
        request.session['many_cities'] = many_cities
        request.session['departure_date'] = departure_date
        request.session['return_date'] = return_date
        request.session['departure_city'] = departure_city
        if not weather:
            return render(request, 'questions/questions.html', {'error_message': 'Please select at least one weather type.'})
        return redirect('results')
    else:
        return render(request, 'questions.html')


def results(request):
    continent = request.session.get('continent')
    weather = request.session.get('weather')
    population = request.session.get('population')
    many_cities = request.session.get('many_cities')
    url = 'https://restcountries.com/v3.1/region/'
    countries = get_countries(url, continent)

    filtered = filter_countries(countries, weather)
    names = [country['name']['common'] for country in filtered]
    countries_id = get_country_id(names)
    filtered = get_cities(countries_id, population, many_cities)

    return render(request, 'results.html', {'continent': continent, 'data_continents': filtered})


def flights(request, country_name, city_name):
    if request.method == 'POST':
        departure_date = request.POST.get('departureDate')
        return_date = request.POST.get('returnDate')
        departure_city = request.POST.get('departureCity')
        arrival_iata = request.POST.get('arrivalIATA')
        request.session['departure_date'] = departure_date
        request.session['return_date'] = return_date
        request.session['departure_city'] = departure_city
        request.session['arrival_iata'] = arrival_iata
    else:
        departure_date = request.session.get('departure_date')
        return_date = request.session.get('return_date')
        departure_city = request.session.get('departure_city')
        arrival_iata = request.session.get('arrival_iata')

    api_key = settings.AVIATIONSTACK_API_KEY

    try:
        # Fetch country information
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

        # Fetch city information
        city_url = 'http://api.aviationstack.com/v1/cities'
        city_params = {
            'access_key': api_key,
            'limit': 1,
            'search': city_name
        }
        city_response = requests.get(city_url, params=city_params)
        city_response.raise_for_status()
        city_data_list = city_response.json().get('data', [])
        if not city_data_list:
            return render(request, 'flights.html', {
                'error_message': 'No city information found.'
            })
        city_data = city_data_list[0]

        # Fetch flight information
        flight_url = 'http://api.aviationstack.com/v1/flights'
        flight_params = {
            'access_key': api_key,
            'dep_iata': departure_city,
            'arr_iata': arrival_iata,
            'flight_date': departure_date,
            'limit': 10
        }
        flight_response = requests.get(flight_url, params=flight_params)
        flight_response.raise_for_status()
        flights_data = flight_response.json().get('data', [])

    except requests.RequestException as e:
        logger.error(f"Error fetching data from API: {e}")
        return render(request, 'flights.html', {
            'error_message': 'There was an error retrieving flight data. Please try again later.'
        })

    return render(request, 'flights.html', {
        'country_name': country_data['country_name'],
        'city_name': city_data['city_name'],
        'departure_country': country_data,
        'departure_city': city_data,
        'flights': flights_data,
        'arrival_iata': arrival_iata
    })


def select_flight(request):
    if request.method == 'POST':
        flight_number = request.POST.get('flight_number')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        departure_airport = request.POST.get('departure_airport')
        arrival_airport = request.POST.get('arrival_airport')

        # Store selected flight details in session
        request.session['selected_flight'] = {
            'flight_number': flight_number,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'departure_airport': departure_airport,
            'arrival_airport': arrival_airport
        }

        # Redirect to the return flights selection page
        return redirect('flights', country_name=request.session.get('arrival_country_name'), city_name=request.session.get('arrival_city_name'))

    return redirect('index')
