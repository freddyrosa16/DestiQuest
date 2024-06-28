from django.http import JsonResponse
from django.shortcuts import render, redirect
from questions.utils import get_countries, filter_countries, get_country_id, get_cities, get_flights
from django.views import View
import requests
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth.signals import user_logged_in


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class CustomLoginView(auth_views.LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        user_logged_in.send(sender=self.__class__,
                            request=self.request, user=self.request.user)
        return response


class IATACodeAutocomplete(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        if query:
            api_url = 'http://api.aviationstack.com/v1/cities'
            params = {
                'access_key': settings.AVIATIONSTACK_API_KEY,
                'search': query,
                'limit': 10
            }
            response = requests.get(api_url, params=params)
            data = response.json()
            suggestions = [
                {'city_name': city['city_name'],
                    'iata_code': city['iata_code']}
                for city in data.get('data', [])
            ]
            return JsonResponse({'suggestions': suggestions})
        return JsonResponse({'suggestions': []})


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
