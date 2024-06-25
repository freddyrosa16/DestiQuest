from django.shortcuts import render, redirect
from .utils import get_countries, filter_countries, get_country_id, get_cities, get_flights


def index(request):
    return render(request, 'main.html')


def questions(request):
    if request.method == 'POST':
        continent = request.POST.get('continent')
        weather = request.POST.getlist('weather')
        population = request.POST.get('population')
        many_cities = request.POST.get('many_cities')
        departure_date = request.POST.get('departureDate')
        departure_city = request.POST.get('departureCity')
        request.session['continent'] = continent
        request.session['weather'] = weather
        request.session['population'] = population
        request.session['many_cities'] = many_cities
        request.session['departure_date'] = departure_date
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
        departure_city = request.POST.get('departureCity')
        arrival_iata = request.POST.get('arrivalIATA')
        request.session['departure_date'] = departure_date
        request.session['departure_city'] = departure_city
        request.session['arrival_iata'] = arrival_iata
    else:
        departure_date = request.session.get('departure_date')
        departure_city = request.session.get('departure_city')
        arrival_iata = request.session.get('arrival_iata')

    print(f"Departure City: {departure_city}")
    print(f"Arrival IATA: {arrival_iata}")
    print(f"Departure Date: {departure_date}")

    api_key = '3866066ab1dc76f06b0b35f3d1ba5bd5'
    flights = get_flights(api_key, departure_city,
                          arrival_iata, departure_date)
    print(f"Flights: {flights}")
    return render(request, 'flights.html', {'country_name': country_name, 'city_name': city_name, 'flights': flights, 'arrival_iata': arrival_iata})
