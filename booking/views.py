from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from qrcode import *
from django.utils import timezone
from .models import Club, Event, Club_Event, Club_Event_Booking, Event_Booking, Issue, Club_Event_Table_Booking, Event_Table_Booking
import json
from django.views.decorators.csrf import csrf_exempt
from Paytm import Checksum
import datetime
MERCHANT_KEY = 'bKMfNxPPf_QdZppa'


# Create your views here.
def index(request):

    if request.method == "POST":

        user_city = request.POST.get('city')
        clubs = Club.objects.all()
        events = Event.objects.filter(event_city=user_city)
        bollywood = Club.objects.filter(club_category='Bollywood').filter(club_city=user_city)
        dance = Club.objects.filter(club_category='Dance').filter(club_city=user_city)
        hiphop = Club.objects.filter(club_category='HipHop').filter(club_city=user_city)
        party = Club.objects.filter(club_category='Party').filter(club_city=user_city)
        params = {'club': clubs, 'event': events, 'bollywood': bollywood, 'dance': dance, 'hiphop': hiphop,
                  'party': party}
        return render(request, 'index.html', params)

    else:

        clubs = Club.objects.all()
        events = Event.objects.all()
        bollywood = Club.objects.filter(club_category='Bollywood')
        dance = Club.objects.filter(club_category='Dance')
        hiphop = Club.objects.filter(club_category='HipHop')
        party = Club.objects.filter(club_category='Party')
        params = {'club':clubs, 'event':events, 'bollywood':bollywood, 'dance':dance, 'hiphop':hiphop, 'party':party}
        return render(request, 'index.html', params)


def searchMatchClub(query, item):
    if query in item.club_name.lower() or query in item.club_category.lower() or query in item.club_city.lower() or query in item.club_about.lower():
        return True
    else:
        return False

def searchMatchEvent(query, item):
    if query in item.event_name.lower() or query in item.artist1.lower() or query in item.artist2.lower() or query in item.artist3.lower() or query in item.event_city.lower() or query in item.event_about.lower():
        return True
    else:
        return False

def searchMatchClubEvent(query, item):
    if query in item.c_event_name.lower() or query in item.artist1.lower() or query in item.artist2.lower() or query in item.artist3.lower() or query in item.club.club_city.lower() or query in item.c_event_about.lower():
        return True
    else:
        return False


def search(request):
    query= request.GET.get('search')
    all_clubs = Club.objects.all()
    all_events = Event.objects.all()
    all_club_events = Club_Event.objects.all()
    clubs = [item for item in all_clubs if searchMatchClub(query, item)]
    events = [item for item in all_events if searchMatchEvent(query, item)]
    club_events = [item for item in all_club_events if searchMatchClubEvent(query, item)]

    params = {'club':clubs, 'event':events, 'c_event':club_events, "msg":""}
    if len(clubs)==0 and len(events)==0 or len(query)<3:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'search.html', params)




def clubList(request):

    if request.method == "POST":

        user_city = request.POST.get('city')
        clubs = Club.objects.filter(club_city=user_city)
        return render(request, 'club/clubList.html', {'club': clubs})

    else:
        clubs = Club.objects.all()
        return render(request, 'club/clubList.html', {'club': clubs})

def clubView(request, myid):

    club = Club.objects.filter(club_id=myid)
    events = Club_Event.objects.filter(club=club[0])
    return render(request, 'club/clubView.html', {'club':club[0], 'events':events})

def clubEventList(request, myid):

    club = Club.objects.filter(club_id=myid)
    events = Club_Event.objects.filter(club=club[0])
    return render(request, 'club/clubEventList.html', {'club': club[0], 'events': events})

def clubEventView(request, myid):

    event = Club_Event.objects.filter(c_event_id=myid)
    return render(request, 'club/clubEventView.html', {'event':event[0]})

def clubEventBooking(request, myid):

        if request.user.is_authenticated:
            event = Club_Event.objects.filter(c_event_id=myid)
            return render(request, 'club/clubEventBooking.html', {'event': event[0]})
        else:
            return redirect('/accounts/login')

def clubEventTableList(request, myid):

    events = Club_Event.objects.filter(c_event_id=myid)
    return render(request, 'club/clubEventTableList.html', {'event':events[0]})


def checkoutClubEvent(request, myid):

    if request.method == "POST":
        males = request.POST.getlist('male')
        females = request.POST.getlist('female')
        couples = request.POST.getlist('couple')

        events = Club_Event.objects.filter(c_event_id=myid)

        myModel = Club_Event_Booking()
        myModel.user = request.user
        myModel.event = events[0]

        myModel.males = json.dumps(males)
        myModel.females = json.dumps(females)
        myModel.couples = json.dumps(couples)
        amount = (len(males) * events[0].male_price) + (len(females) * events[0].female_price) + (len(couples) * events[0].couple_price/2)
        tax = amount*0.18
        myModel.amount= amount + tax
        myModel.time_stamp= timezone.now()
        myModel.save()

        total_no = len(males) + len(females) + len(couples)

        params = {'event': events[0], 'booking':myModel, 'no_males':len(males), 'no_females':len(females), 'no_couples':len(couples)//2, 'amount':amount, 'tax':tax, 'total_no':total_no}

        return render(request, 'club/checkoutClubEvent.html', params)
    else:
        return redirect("/club")


def checkoutClubEventTable(request, myid):
    if request.user.is_authenticated:
        myid_first = myid

        while (myid_first >= 10):
            myid_first = myid_first // 10

        id = myid - myid_first * (10 ** len(str(myid))/10)

        events = Club_Event.objects.filter(c_event_id=id)

        amount = myid_first * events[0].male_price
        tax = amount * 0.18
        total_amount = amount + tax

        myModel = Club_Event_Table_Booking()
        myModel.user = request.user
        myModel.event = events[0]
        myModel.table = myid_first
        myModel.amount = total_amount
        myModel.time_stamp = timezone.now()
        myModel.save()

        params = {'event': events[0], 'booking': myModel, 'amount': amount, 'tax': tax, 'total_no': myid_first}

        return render(request, 'club/checkoutClubEventTable.html', params)

    else:
        return redirect('/accounts/login')



def paymentClubEvent(request, myid):

    booking = Club_Event_Booking.objects.filter(booking_id=myid)
    id = str(booking[0].user) + ".ce" + str(booking[0].event.c_event_id) + "." + str(myid)
    amount = booking[0].amount
    useremail = booking[0].user.email

    param_dict = {

        'MID': 'DIY12386817555501617',
        'ORDER_ID': id,
        'TXN_AMOUNT': str(amount),
        'CUST_ID': useremail,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'https://nightlife-django-thegrayfox.herokuapp.com/handlerequestClubEvent/',

    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'paytm.html', {'param_dict': param_dict})

def paymentClubEventTable(request, myid):

    booking = Club_Event_Table_Booking.objects.filter(booking_id=myid)
    id = str(booking[0].user) + ".cet" + str(booking[0].event.c_event_id) + "." + str(myid)
    amount = booking[0].amount
    useremail = booking[0].user.email

    param_dict = {

        'MID': 'DIY12386817555501617',
        'ORDER_ID': id,
        'TXN_AMOUNT': str(amount),
        'CUST_ID': useremail,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'https://nightlife-django-thegrayfox.herokuapp.com/handlerequestClubEventTable/',

    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'paytm.html', {'param_dict': param_dict})

@csrf_exempt
def handlerequestClubEvent(request):
    # paytm will send you post request here

    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    id = response_dict['ORDERID'].split('.')[2]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            Club_Event_Booking.objects.filter(booking_id=id).update(payment_status="Paid", time_stamp=response_dict['TXNDATE'], finalbooking_id=response_dict['ORDERID'])
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            Club_Event_Booking.objects.filter(booking_id=id).update(payment_status="Pending")

    booking = Club_Event_Booking.objects.filter(booking_id=id)

    return render(request, 'club/paymentstatusClubEvent.html', {'response': response_dict, 'booking':booking[0]})

@csrf_exempt
def handlerequestClubEventTable(request):
    # paytm will send you post request here

    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    id = response_dict['ORDERID'].split('.')[2]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            Club_Event_Table_Booking.objects.filter(booking_id=id).update(payment_status="Paid", time_stamp=response_dict['TXNDATE'], finalbooking_id=response_dict['ORDERID'])
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            Club_Event_Table_Booking.objects.filter(booking_id=id).update(payment_status="Pending")

    booking = Club_Event_Table_Booking.objects.filter(booking_id=id)

    return render(request, 'club/paymentstatusClubEventTable.html', {'response': response_dict, 'booking':booking[0]})


def bookingDetailsClubEvent(request, myid):

    booking = Club_Event_Booking.objects.filter(booking_id=myid)

    males = booking[0].males.split(',')
    if males[0] == "[]":
        len_males = 0
    else:
        len_males = len(males)

    females = booking[0].females.split(',')
    if females[0] == "[]":
        len_females = 0
    else:
        len_females = len(females)

    couples = booking[0].couples.split(',')
    if couples[0] == "[]":
        len_couples = 0
    else:
        len_couples = len(couples)

    total_no = len_males + len_females + len_couples

    url = "/club/event/booking/" + str(booking[0].booking_id)
    img = make(url)
    save_url = "static/images/"+str(booking[0].user)+"_ce_booking"+str(booking[0].booking_id)+".png"
    img.save(save_url)



    return render(request, 'club/bookingDetailsClubEvent.html', {'booking':booking[0], 'total_no':total_no})

def bookingDetailsClubEventTable(request, myid):

    booking = Club_Event_Table_Booking.objects.filter(booking_id=myid)

    url = "/club/event/bookingTable/" + str(booking[0].booking_id)
    img = make(url)
    save_url = "static/images/"+str(booking[0].user)+"_cet_booking"+str(booking[0].booking_id)+".png"
    img.save(save_url)

    amount = booking[0].amount // 1.18
    total_no = amount // booking[0].event.male_price
    table = booking[0]


    return render(request, 'club/bookingDetailsClubEventTable.html', {'booking':booking[0], 'total_no':int(total_no), 'table':table})









def eventList(request):
    today_date = datetime.date.today()
    tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)
    today1 = Event.objects.filter(event_date=today_date)
    tomorrow1 = Event.objects.filter(event_date=tomorrow_date)
    date_query = request.GET.get('date')
    date = Event.objects.filter(event_date=date_query)



    if request.method == "POST":

        user_city = request.POST.get('city')
        today = today1.filter(event_city=user_city)
        tomorrow = tomorrow1.filter(event_city=user_city)
        weekend = list(Event.objects.filter(event_date__week_day=1).filter(event_city=user_city)) + list(Event.objects.filter(event_date__week_day=7).filter(event_city=user_city))
        calendar = date.filter(event_city=user_city)

        return render(request, 'event/eventList.html', {'today': today, 'tomorrow':tomorrow, 'weekend':weekend, 'calendar':calendar})

    else:
        today = Event.objects.filter(event_date=today_date)
        tomorrow = Event.objects.filter(event_date=tomorrow_date)
        weekend = list(Event.objects.filter(event_date__week_day=1)) + list(
            Event.objects.filter(event_date__week_day=7))

        return render(request, 'event/eventList.html', {'today': today, 'tomorrow':tomorrow, 'weekend':weekend, 'calendar':date})

def eventView(request, myid):

    events = Event.objects.filter(event_id=myid)
    return render(request, 'event/eventView.html', {'event':events[0]})


def eventBooking(request, myid):
    if request.user.is_authenticated:
        event = Event.objects.filter(event_id=myid)
        return render(request, 'event/eventBooking.html', {'event': event[0]})
    else:
        return redirect('/accounts/login')

def eventTableList(request, myid):

    events = Event.objects.filter(event_id=myid)
    return render(request, 'event/eventTableList.html', {'event':events[0]})


def eventTableBooking(request, myid):

    events = Event.objects.filter(event_id=myid)
    return render(request, 'event/checkoutEvent.html', {'event':events[0]})

def checkoutEvent(request, myid):

    if request.method == "POST":
        males = request.POST.getlist('male')
        females = request.POST.getlist('female')
        couples = request.POST.getlist('couple')

        events = Event.objects.filter(event_id=myid)

        myModel = Event_Booking()
        myModel.user = request.user
        myModel.event = events[0]

        myModel.males = json.dumps(males)
        myModel.females = json.dumps(females)
        myModel.couples = json.dumps(couples)
        amount = (len(males) * events[0].event_price) + (len(females) * events[0].event_price) + (len(couples) * events[0].event_price/2)
        tax = amount*0.18
        myModel.amount= amount + tax
        myModel.time_stamp= timezone.now()
        myModel.save()

        total_no = len(males) + len(females) + len(couples)

        params = {'event': events[0], 'booking':myModel, 'no_males':len(males), 'no_females':len(females), 'no_couples':len(couples)//2, 'amount':amount, 'tax':tax, 'total_no':total_no}

        return render(request, 'event/checkoutEvent.html', params)
    else:
        return redirect("/event")


def checkoutEventTable(request, myid):
    if request.user.is_authenticated:
        myid_first = myid

        while (myid_first >= 10):
            myid_first = myid_first // 10

        print(myid_first)
        print(myid)

        id = myid - myid_first * (10 ** len(str(myid))/10)
        print(id)

        events = Event.objects.filter(event_id=id)

        amount = myid_first * events[0].event_price
        tax = amount * 0.18
        total_amount = amount + tax

        myModel = Event_Table_Booking()
        myModel.user = request.user
        myModel.event = events[0]
        myModel.table = myid_first
        myModel.amount = total_amount
        myModel.time_stamp = timezone.now()
        myModel.save()

        params = {'event': events[0], 'booking': myModel, 'amount': amount, 'tax': tax, 'total_no': myid_first}

        return render(request, 'event/checkoutEventTable.html', params)

    else:
        return redirect('/accounts/login')



def paymentEvent(request, myid):

    booking = Event_Booking.objects.filter(booking_id=myid)
    id = str(booking[0].user) + ".e" + str(booking[0].event.event_id) + "." + str(myid)
    amount = booking[0].amount
    useremail = booking[0].user.email

    param_dict = {

        'MID': 'DIY12386817555501617',
        'ORDER_ID': id,
        'TXN_AMOUNT': str(amount),
        'CUST_ID': useremail,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'https://nightlife-django-thegrayfox.herokuapp.com/handlerequestEvent/',

    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'paytm.html', {'param_dict': param_dict})

def paymentEventTable(request, myid):

    booking = Event_Table_Booking.objects.filter(booking_id=myid)
    id = str(booking[0].user) + ".et" + str(booking[0].event.event_id) + "." + str(myid)
    amount = booking[0].amount
    useremail = booking[0].user.email

    param_dict = {

        'MID': 'DIY12386817555501617',
        'ORDER_ID': id,
        'TXN_AMOUNT': str(amount),
        'CUST_ID': useremail,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'https://nightlife-django-thegrayfox.herokuapp.com/handlerequestEventTable/',

    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'paytm.html', {'param_dict': param_dict})

@csrf_exempt
def handlerequestEvent(request):
    # paytm will send you post request here

    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    id = response_dict['ORDERID'].split('.')[2]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            Event_Booking.objects.filter(booking_id=id).update(payment_status="Paid", time_stamp=response_dict['TXNDATE'], finalbooking_id=response_dict['ORDERID'])
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            Event_Booking.objects.filter(booking_id=id).update(payment_status="Pending")

    booking = Event_Booking.objects.filter(booking_id=id)

    return render(request, 'event/paymentstatusEvent.html', {'response': response_dict, 'booking':booking[0]})

@csrf_exempt
def handlerequestEventTable(request):
    # paytm will send you post request here

    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    id = response_dict['ORDERID'].split('.')[2]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            Event_Table_Booking.objects.filter(booking_id=id).update(payment_status="Paid", time_stamp=response_dict['TXNDATE'], finalbooking_id=response_dict['ORDERID'])
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            Event_Table_Booking.objects.filter(booking_id=id).update(payment_status="Pending")

    booking = Event_Table_Booking.objects.filter(booking_id=id)

    return render(request, 'event/paymentstatusEventTable.html', {'response': response_dict, 'booking':booking[0]})


def bookingDetailsEvent(request, myid):

    booking = Event_Booking.objects.filter(booking_id=myid)

    males = booking[0].males.split(',')
    if males[0] == "[]":
        len_males = 0
    else:
        len_males = len(males)

    females = booking[0].females.split(',')
    if females[0] == "[]":
        len_females = 0
    else:
        len_females = len(females)

    couples = booking[0].couples.split(',')
    if couples[0] == "[]":
        len_couples = 0
    else:
        len_couples = len(couples)

    total_no = len_males + len_females + len_couples

    url = "/event/booking/" + str(booking[0].booking_id)
    img = make(url)
    save_url = "static/images/" + str(booking[0].user) + "_e_booking" + str(booking[0].booking_id)+ ".png"
    img.save(save_url)



    return render(request, 'event/bookingDetailsEvent.html', {'booking':booking[0], 'total_no':total_no})

def bookingDetailsEventTable(request, myid):

    booking = Event_Table_Booking.objects.filter(booking_id=myid)

    url = "/event/bookingTable/" + str(myid)
    img = make(url)
    save_url = "static/images/"+str(booking[0].user)+"_et_booking"+str(myid)+".png"
    img.save(save_url)

    amount = booking[0].amount // 1.18
    total_no = amount // booking[0].event.event_price
    table = booking[0]


    return render(request, 'event/bookingDetailsEventTable.html', {'booking':booking[0], 'total_no':int(total_no), 'table':table})








def bookingListView(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            club_bookings = Club_Event_Booking.objects.filter(payment_status="Paid")
            club_table_bookings = Club_Event_Table_Booking.objects.filter(payment_status="Paid")
            event_bookings = Event_Booking.objects.filter(payment_status="Paid")
            event_table_bookings = Event_Table_Booking.objects.filter(payment_status="Paid")
            return render(request, 'bookingListView.html', {'club_bookings':club_bookings,'event_bookings':event_bookings,'event_table_bookings':event_table_bookings, 'club_table_bookings':club_table_bookings })
        else:
            club_bookings = Club_Event_Booking.objects.filter(user=request.user, payment_status="Paid")
            club_table_bookings = Club_Event_Table_Booking.objects.filter(user=request.user, payment_status="Paid")
            event_bookings = Event_Booking.objects.filter(user=request.user, payment_status="Paid")
            return render(request, 'bookingListView.html',
                          {'club_bookings': club_bookings, 'event_bookings': event_bookings, 'club_table_bookings':club_table_bookings })
    else:
        return redirect('/accounts/login')


def settings(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            club_bookings = Club_Event_Booking.objects.all()
            event_bookings = Event_Booking.objects.all()
            return render(request, 'account/settings.html', {'club_bookings':club_bookings,'event_bookings':event_bookings })
        else:
            club_bookings = Club_Event_Booking.objects.filter(user=request.user)
            event_bookings = Event_Booking.objects.filter(user=request.user)
            return render(request, 'account/settings.html',
                          {'club_bookings': club_bookings, 'event_bookings': event_bookings})
    else:
        return redirect('/accounts/login')

def offers(request):
    if request.user.is_authenticated:
        return render(request, 'offers.html')
    else:
        return redirect('/accounts/login')

def faq(request):
    if request.user.is_authenticated:
        return render(request, 'faq.html')
    else:
        return redirect('/accounts/login')


def helpSupport(request):

    thank = False
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('tel')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        myModel = Issue()
        myModel.name = name

        myModel.email = email
        myModel.phone = phone
        myModel.subject = subject
        myModel.userissue = message
        myModel.save()
        thank = True

        return render(request, 'helpSupport.html', {'thank':thank})

    else:
        if request.user.is_authenticated:
            return render(request, 'helpSupport.html', {'thank':thank})
        else:
            return redirect('/accounts/login')


