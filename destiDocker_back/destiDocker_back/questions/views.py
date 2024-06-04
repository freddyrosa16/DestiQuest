from django.shortcuts import render, redirect
import requests
import time

# Create your views here.
def index(request):
    return render(request, 'index.html')

def questions(request):
    if request.method == 'POST':
        continent = request.POST.get('continent')
        request.session['continent'] = continent
        return redirect('results')
    else: 
        return render(request, 'questions.html')

def results(request):
    continent = request.session.get('continent')
    
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    param = {
        "query": f"cities in {continent}",
        "key": "AIzaSyDJsxyUDBlOaUAalBvUdVrlw-DX-KZ-Jig"
    }
    
    cities = []
    
    while True:
        response = requests.get(url, params=param)
        data = response.json()
        cities.extend([result['name'] for result in data['results']])
        if 'next_page_token' in data:
            param['pagetoken'] = data['next_page_token']
            
            time.sleep(5)
        else:
            break
    
    context = {"cities": cities, "continent": continent}
    return render(request, 'results.html', context)