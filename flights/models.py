from django.db import models
from datetime import datetime
class Place(models.Model):
    city = models.CharField(max_length=64,null=True)
    airport = models.CharField(max_length=64,null=True)
    code = models.CharField(max_length=3,null=True)
    country = models.CharField(max_length=64,null=True)

    def __str__(self):
        return f"{self.city}, {self.country} ({self.code})"


class Week(models.Model):
    """Week model for storing days of the week."""
    number = models.IntegerField(unique=True)  # Store weekday number (0-6 for Mon-Sun)
    name = models.CharField(max_length=20)     # Store the name of the day (e.g., 'Monday')

    def __str__(self):
        return self.name


class Flight(models.Model):
    
    origin = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="departures",null=True)
    destination = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="arrivals",null=True)
    depart_time = models.TimeField(auto_now=False, auto_now_add=False,null=True)
    depart_day = models.ManyToManyField(Week, related_name="flights_of_the_day")
    duration = models.DurationField(null=True)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False,null=True)
    plane = models.CharField(max_length=24,null=True)
    airline = models.CharField(max_length=64,null=True)
    economy_fare = models.FloatField(null=True)
    business_fare = models.FloatField(null=True)
    first_fare = models.FloatField(null=True)

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

   