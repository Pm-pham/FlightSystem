from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from flights.models import Flight

SEAT_CLASS = (
    ('economy', 'Economy'),
    ('business', 'Business'),
    ('first', 'First')
)

TICKET_STATUS =(
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled')
)
class Passenger(models.Model):
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    gender = models.CharField(max_length=20,null=True)

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", blank=True, null=True)
    passengers = models.ManyToManyField(Passenger, related_name="flight_tickets")
    ref_no = models.CharField(max_length=6, unique=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets", blank=True, null=True)
    flight_ddate = models.DateField(blank=True, null=True)
    flight_adate = models.DateField(blank=True, null=True)
    flight_fare = models.FloatField(blank=True, null=True)
    other_charges = models.FloatField(blank=True, null=True)
    coupon_used = models.CharField(max_length=15, blank=True)
    coupon_discount = models.FloatField(default=0.0)
    total_fare = models.FloatField(blank=True, null=True)
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    booking_date = models.DateTimeField(default=datetime.now)
    mobile = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=45, blank=True)
    status = models.CharField(max_length=45, choices=TICKET_STATUS)


class Payment(models.Model):
    STATUS = (
        (0, "paid"),
        (1, "pending"),
        (2, "failed"),
    )
    fare = models.DecimalField(decimal_places=2, max_digits=18)
    card_number = models.CharField(max_length=20, null=True)
    card_holder_name = models.CharField(max_length=150, null=True)
    expMonth = models.IntegerField(null=True)
    expYear = models.IntegerField(null=True)
    cvv =  models.IntegerField(null=True)
    status = models.CharField(default=STATUS[0][1],max_length=20, null=True)
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
    ticket_id2 = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True,related_name="payment_tickets2")



