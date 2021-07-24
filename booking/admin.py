from django.contrib import admin
from .models import Club, Event, Club_Event, Club_Event_Booking, Event_Booking, Issue, Club_Event_Table_Booking, Event_Table_Booking

# Register your models here.
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(Club_Event_Booking)
admin.site.register(Event_Booking)
admin.site.register(Club_Event)
admin.site.register(Issue)
admin.site.register(Club_Event_Table_Booking)
admin.site.register(Event_Table_Booking)