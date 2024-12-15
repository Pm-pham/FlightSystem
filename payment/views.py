from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
import secrets
from flights.constant import FEE
from flights.models import Flight
from payment.models import Payment, Passenger, Ticket
from frontend.template import *

def payment_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # lấy dữ liệu trên form
            ticket1_id = request.POST.get("ticket1")
            print(ticket1_id)
            fare = request.POST.get("fare")
            cardNumber = request.POST.get('cardNumber')
            cardHolderName = request.POST.get('cardHolderName')
            expMonth = int(request.POST.get('expMonth'))
            expYear = int(request.POST.get('expYear'))
            cvv = request.POST.get('cvv')
            # Lấy ngày tháng năm hiện tại.
            current_year = datetime.today().year
            current_month = datetime.today().month
            t2 = False
            if request.POST.get('ticket2'):
                t2 = True
                ticket2_id = request.POST.get('ticket2')
            try:
                ticket = Ticket.objects.get(id=ticket1_id)
                ticket.status = 'PENDING'
                ticket.booking_date = datetime.now()
                tics = {'ticket1': ticket1_id,
                        'fare': fare}
                ticket.save()
                # Nếu thẻ còn hạn thì tạo thanh toán
                payment = Payment.objects.create(
                    fare=fare,
                    card_number=cardNumber,
                    card_holder_name=cardHolderName,
                    expMonth=expMonth,
                    expYear=expYear,
                    cvv=cvv,
                    ticket_id=ticket,
                    status='PENDING',
                )
                if t2:
                    ticket2 = Ticket.objects.get(id=ticket2_id)
                    ticket2.status = 'PENDING'
                    ticket2.booking_date = datetime.now()
                    ticket2.save()
                    tics = {'ticket1': ticket1_id,
                            'ticket2': ticket2_id,
                            'fare' : fare,}
                    payment.ticket_id2 = ticket2
                    # Kiểm tra số của thẻ có dưới 12 chữ số hay không. Không thì báo lỗi
                if len(cardNumber) < 12:
                    messages.warning(request, 'Card number must be at least 12 digits')
                    return render(request, 'payment.html', tics)
                        # Kiểm tra xem thời gian hiệu lực của thẻ
                if expYear < current_year or (expYear == current_year and expMonth < current_month):
                    messages.warning(request, 'Card expired')
                    return render(request, 'payment.html', tics)
                tics = {'ticket1':ticket}
                if t2:
                    ticket2.status = 'CONFIRMED'
                    ticket2.save()
                    tics = {'ticket1':ticket,'ticket2':ticket2}
                ticket.status = 'CONFIRMED'
                ticket.save()
                payment.status = 'CONFIRMED'
                payment.save()
                return render(request, 'payment_process.html',tics)
            except Exception as e:
                return HttpResponse(e)
    else:
        return HttpResponseRedirect(reverse('login'))

def ticket_data(request, ref):
    ticket = Ticket.objects.get(ref_no=ref)
    return JsonResponse({
        'ref': ticket.ref_no,
        'from': ticket.flight.origin.code,
        'to': ticket.flight.destination.code,
        'flight_date': ticket.flight_ddate,
        'status': ticket.status
    })

def book(request):
    fare = 0
    if request.method == 'POST':
        if request.user.is_authenticated:
            flight1 = Flight.objects.get(id=request.POST.get('flight1'))
            flight_1date = request.POST.get('flight1Date')
            flight_1class = request.POST.get('flight1Class')
            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            email = request.POST['email']
            f2 = False
            flight2 = None
            flight_2date = None
            flight_2class = None
            if request.POST.get('flight2'):
                flight2 = Flight.objects.get(id=request.POST.get('flight2'))
                flight_2date = request.POST.get('flight2Date')
                flight_2class = request.POST.get('flight2Class')
                f2 = True
            passengerscount = request.POST['passengersCount']
            passengers = []
            for i in range(1, int(passengerscount) + 1):
                fname = request.POST[f'passenger{i}FName']
                lname = request.POST[f'passenger{i}LName']
                gender = request.POST[f'passenger{i}Gender']
                passengers.append(Passenger.objects.create(first_name=fname, last_name=lname, gender=gender.lower()))
            coupon = request.POST.get('coupon')
            ticket2 = None
            try:
                fare_ticket1 = 0
                fare_ticket2 = 0
                ticket1 = createticket(request.user,passengers,passengerscount,flight1,flight_1date,flight_1class,coupon,countrycode,email,mobile)
                ticket1.status = 'PENDING'
                if f2:
                    ticket2 = createticket(request.user,passengers,passengerscount,flight2,flight_2date,flight_2class,coupon,countrycode,email,mobile)
                    ticket2.status = 'PENDING'
                if(flight_1class == 'Economy'):
                    fare_ticket1 = (flight1.economy_fare * int(passengerscount))
                    if f2:
                        fare_ticket2 = (flight2.economy_fare * int(passengerscount))
                if (flight_1class == 'Business'):
                    fare_ticket1 = (flight1.business_fare * int(passengerscount))
                    if f2:
                        fare_ticket2 = (flight2.business_fare * int(passengerscount))
                if (flight_1class == 'First'):
                    fare_ticket1 = (flight1.first_fare * int(passengerscount))
                    if f2:
                        fare_ticket2 = (flight2.first_fare * int(passengerscount))
                fare = fare_ticket1 + fare_ticket2
            except Exception as e:
                return HttpResponse(e)
            ticket1.total_fare = fare_ticket1
            ticket1.save()
            if f2:
                ticket2.total_fare = fare_ticket2
                ticket2.save()
                return render(request, "payment.html", { ##
                    'fare': fare + FEE,  ##
                    'ticket1': ticket1.pk,  ##
                    'ticket2': ticket2.pk  ##
                })  ##
            return render(request, "payment.html", {
                'fare': fare + FEE,
                'ticket1': ticket1.pk
            })
        else:
            return HttpResponse("Method must be post.")

def createticket(user,passengers,passengerscount,flight1,flight_1date,flight_1class,coupon,countrycode,email,mobile):
    ticket = Ticket.objects.create()
    ticket.user = user
    ticket.ref_no = secrets.token_hex(3).upper()
    for passenger in passengers:
        ticket.passengers.add(passenger)
    ticket.flight = flight1
    ticket.flight_ddate = datetime(int(flight_1date.split('-')[2]),int(flight_1date.split('-')[1]),int(flight_1date.split('-')[0]))
    ###################
    flight1ddate = datetime(int(flight_1date.split('-')[2]),int(flight_1date.split('-')[1]),int(flight_1date.split('-')[0]),flight1.depart_time.hour,flight1.depart_time.minute)
    flight1adate = (flight1ddate + flight1.duration)
    ###################
    ticket.flight_adate = datetime(flight1adate.year,flight1adate.month,flight1adate.day)
    ffre = 0.0
    if flight_1class.lower() == 'first':
        ticket.flight_fare = flight1.first_fare*int(passengerscount)
        ffre = flight1.first_fare*int(passengerscount)
    elif flight_1class.lower() == 'business':
        ticket.flight_fare = flight1.business_fare*int(passengerscount)
        ffre = flight1.business_fare*int(passengerscount)
    else:
        ticket.flight_fare = flight1.economy_fare*int(passengerscount)
        ffre = flight1.economy_fare*int(passengerscount)
    ticket.other_charges = FEE
    if coupon:
        ticket.coupon_used = coupon                     ##########Coupon
    ticket.total_fare = ffre+FEE+0.0                    ##########Total(Including coupon)
    ticket.seat_class = flight_1class.lower()
    ticket.status = 'PENDING'
    ticket.mobile = ('+'+countrycode+' '+mobile)
    ticket.email = email
    ticket.save()
    return ticket