from django.shortcuts import render, redirect
from .utils import get_countries, filter_countries, get_country_id, get_cities, get_flights


def index(request):
    return render(request, 'index.html')


def questions(request):
    if request.method == 'POST':
        continent = request.POST.get('continent')
        weather = request.POST.getlist('weather')
        population = request.POST.get('population')
        many_cities = request.POST.get('many_cities')
        departure_date = request.POST.get('departureDate')
        request.session['continent'] = continent
        request.session['weather'] = weather
        request.session['population'] = population
        request.session['many_cities'] = many_cities
        request.session['departure_date'] = departure_date
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


def flights(request, country_name):
    departure_date = request.session.get('departure_date')
    flights = get_flights(country_name, departure_date)
    return render(request, 'flights.html', {'country_name': country_name, 'flights': flights})
