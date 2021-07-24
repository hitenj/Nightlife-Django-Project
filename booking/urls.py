from django.urls import path, include
from booking import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


    path('', views.index, name='home'),
    path('search', views.search, name='search'),
    path('paymentClubEvent/<int:myid>', views.paymentClubEvent, name='paymentClubEvent'),
    path('paymentClubEventTable/<int:myid>', views.paymentClubEventTable, name='paymentClubEventTable'),
    path("handlerequestClubEvent/", views.handlerequestClubEvent, name="HandleRequestClubEvent"),
    path("handlerequestClubEventTable/", views.handlerequestClubEventTable, name="HandleRequestClubEventTable"),
    path("club/event/booking/<int:myid>", views.bookingDetailsClubEvent, name="bookingDetailsClubEvent"),
    path("club/event/bookingTable/<int:myid>", views.bookingDetailsClubEventTable, name="bookingDetailsClubEventTable"),

    path('paymentEvent/<int:myid>', views.paymentEvent, name='paymentEvent'),
    path('paymentEventTable/<int:myid>', views.paymentEventTable, name='paymentEventTable'),
    path("handlerequestEvent/", views.handlerequestEvent, name="HandleRequestEvent"),
    path("handlerequestEventTable/", views.handlerequestEventTable, name="HandleRequestEventTable"),
    path("event/booking/<int:myid>", views.bookingDetailsEvent, name="bookingDetailsEvent"),
    path("event/bookingTable/<int:myid>", views.bookingDetailsEventTable, name="bookingDetailsEventTable"),

    path('accounts/settings', views.settings, name='settings'),
    path('offers', views.offers, name='offers'),
    path('faq', views.faq, name='faq'),
    path('helpandsupport', views.helpSupport, name='helpSupport'),
    path('club', views.clubList, name='clubList'),
    path('accounts/bookings', views.bookingListView, name='bookingListView'),

    path("club/<int:myid>", views.clubView, name='clubView'),
    path("club/<int:myid>/events", views.clubEventList, name='clubEventList'),
    path("club/event/<int:myid>", views.clubEventView, name='clubEventView'),
    path('club/event/<int:myid>/book', views.clubEventBooking, name='clubEventBooking'),
    path('club/event/<int:myid>/selecttable', views.clubEventTableList, name='clubEventTableList'),
    path('club/event/<int:myid>/checkout', views.checkoutClubEvent, name='checkoutClubEvent'),
    path('club/event/<int:myid>/booktable', views.checkoutClubEventTable, name='checkoutClubEventTable'),

    path('event', views.eventList, name='eventList'),
    path("event/<int:myid>", views.eventView, name='eventView'),
    path('event/<int:myid>/book', views.eventBooking, name='eventBooking'),
    path('event/<int:myid>/selecttable', views.eventTableList, name='eventTableList'),
    path('event/<int:myid>/booktable', views.checkoutEventTable, name='checkoutEventTable'),
    path('event/<int:myid>/checkout', views.checkoutEvent, name='checkoutEvent'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)