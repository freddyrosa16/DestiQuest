from django.conf import settings
from django.db import models


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    flight_number = models.CharField(max_length=20)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.flight_number}'
