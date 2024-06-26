from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('questions/', views.questions, name='questions'),
    path('questions/results/', views.results, name='results'),
    path('flights/<str:country_name>/<str:city_name>/',
         views.flights, name='flights'),
    path('book_flight/', views.book_flight, name='book_flight'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('booking_confirmation/<int:booking_id>/',
         views.booking_confirmation, name='booking_confirmation'),
]
