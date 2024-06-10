from django.shortcuts import render, redirect
import requests
import json
import urllib

# Create your views here.
def index(request):
    return render(request, 'index.html')

def questions(request):
    if request.method == 'POST':
        continent = request.POST.get('continent')
        weather = request.POST.get('weather')
        request.session['continent'] = continent
        request.session['weather'] = weather
        return redirect('results')
    else: 
        return render(request, 'questions.html')

def results(request):
    continent = request.session.get('continent')
    weather = request.session.get('weather')

    url = f'https://restcountries.com/v3.1/region/{continent.lower()}'

    response = requests.get(url)
    response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx

    data_continents = response.json()
    countries = [country for country in data_continents]

    if weather == 'hot':
        filtered_countries = [country for country in countries if -23.5 <= country['latlng'][0] <= 23.5]
    elif weather == 'cold':
        filtered_countries = [country for country in countries if country['latlng'][0] < -66.5 or country['latlng'][0] > 66.5]
    else:  # templado 
        filtered_countries = [country for country in countries if -66.5 < country['latlng'][0] < 66.5 and not -23.5 <= country['latlng'][0] <= 23.5]

    return render(request, 'results.html', {'continent': continent, 'data_continents': filtered_countries})
