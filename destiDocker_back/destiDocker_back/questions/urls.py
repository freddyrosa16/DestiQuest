from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('questions/', views.questions, name='questions'),
    path('questions/results/', views.results, name='results'),
    path('flights/<str:country_name>/<str:city_name>/',
         views.flights, name='flights'),
]
