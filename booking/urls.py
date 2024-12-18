from django.urls import path
from booking import views

urlpatterns = [
    path('bookings/', views.bookings, name="bookings"),
    path('cancel/', views.cancel_ticket, name="cancelTicket"),
    path('resume/', views.resume_booking, name="resumeBooking"),
]
