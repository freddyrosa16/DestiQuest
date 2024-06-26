# destiDocker_back/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect
from questions.utils import get_countries, filter_countries, get_country_id, get_cities, get_flights  # Updated import
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
        # User will be saved to the database here.
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
