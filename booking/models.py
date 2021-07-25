from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your models here.

# specifying choices

CATEGORIES_CHOICES = (
	("Bollywood", "Bollywood"),
	("HipHop", "HipHop"),
	("Dance", "Dance"),
	("Party", "Party")
)

# declaring a Student Model
class Club(models.Model):
    club_id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=122)
    club_category = models.CharField(
        max_length=20,
        choices=CATEGORIES_CHOICES
    )
    club_address = models.CharField(max_length=122, default="Vinay Building Road, Kandiwali West")
    club_city = models.CharField(max_length=30)
    club_zip_code = models.IntegerField(default=785412)
    club_about = models.TextField(default="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.")
    club_image = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    menus_image = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    ambience_image1 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    ambience_image2 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    club_reg_date = models.DateField()

    def __str__(self):
        return f'{self.club_name}, {self.club_city}'


class Club_Event(models.Model):
    club = models.ForeignKey(Club, null=True, blank=True,
                      on_delete=models.CASCADE)
    c_event_id = models.AutoField(primary_key=True)
    c_event_name = models.CharField(max_length=122)
    c_event_date = models.DateField()
    c_event_time = models.TimeField()
    male_price = models.IntegerField(default=250)
    female_price = models.IntegerField(default=250)
    couple_price = models.IntegerField(default=250)
    c_event_about = models.TextField(
        default="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.")
    event_thumbnail = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    artist_image1 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    artist1 = models.CharField(max_length=122)
    artist_image2 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    artist2 = models.CharField(max_length=122)
    artist_image3 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    artist3 = models.CharField(max_length=122)


    def __str__(self):
        return f'{self.c_event_name} in Club {self.club.club_name}, {self.club.club_city} '


PAYMENT_STATUS = (
	("Not Paid", "Not Paid"),
	("Pending", "Pending"),
	("Paid", "Paid")
)


class Club_Event_Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE)
    event = models.ForeignKey(Club_Event, on_delete=models.CASCADE, null=True)
    males = models.TextField(null=True)
    females = models.TextField(null=True)
    couples = models.TextField(null=True)  # JSON-serialized (text) version of your list
    amount = models.IntegerField(default=0)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default=PAYMENT_STATUS[0][0]
    )
    time_stamp = models.DateTimeField()
    finalbooking_id = models.CharField(default="", max_length=50)




    """ TO RETRIEVE THE LIST FROM DATABASE

    jsonDec = json.decoder.JSONDecoder()
    myPythonList = jsonDec.decode(myModel.myList)"""

    def __str__(self):
        return f'{self.user} has booked on {self.time_stamp} for  {self.event}'

TABLE_CHOICES = (
	(6, "Diamond Table"),
	(7, "Platinum Table"),
	(8, "Royal Table")
)

class Club_Event_Table_Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE)
    event = models.ForeignKey(Club_Event, on_delete=models.CASCADE, null=True)
    table = models.CharField(
        max_length=20,
        choices=TABLE_CHOICES,
        default=TABLE_CHOICES[0][0]
    )
    amount = models.IntegerField(default=0)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default=PAYMENT_STATUS[0][0]
    )
    time_stamp = models.DateTimeField()
    finalbooking_id = models.CharField(default="", max_length=50)

    def __str__(self):
        return self.payment_status





class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=122)
    event_address = models.CharField(max_length=122, default="Vinay Building Road, Kandiwali West")
    event_city = models.CharField(max_length=30)
    event_zip_code = models.IntegerField(default=785412)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_price = models.IntegerField(default=250)
    event_about = models.TextField(default="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.")
    event_thumbnail = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    artist_image1 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    artist1 = models.CharField(max_length=122)
    artist_image2 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    artist2 = models.CharField(max_length=122)
    artist_image3 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    artist3 = models.CharField(max_length=122)
    event_image1 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    event_image2 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    event_image3 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    event_image4 = models.ImageField(upload_to='images', default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    event_image5 = models.ImageField(upload_to='images',
                                     default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    event_image6 = models.ImageField(upload_to='images',
                                     default="images\sam-mar-OQOKSsj8QME-unsplash_yb1Q7yu.jpg")
    event_TC = models.TextField()

    def __str__(self):
        return f'{self.event_name} in {self.event_city}'


class Event_Booking(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    booking_id = models.AutoField(primary_key=True)
    males = models.TextField(null=True)
    females = models.TextField(null=True)
    couples = models.TextField(null=True)
    amount = models.IntegerField(default=0)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default=PAYMENT_STATUS[0][0]
    )
    time_stamp = models.DateTimeField()
    finalbooking_id = models.CharField(default="", max_length=50)


    def __str__(self):
        return f'{self.user} has booked for  {self.event}'


class Event_Table_Booking(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    booking_id = models.AutoField(primary_key=True)
    table = models.CharField(
        max_length=20,
        choices=TABLE_CHOICES,
        default=TABLE_CHOICES[0][0]
    )
    amount = models.IntegerField(default=0)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default=PAYMENT_STATUS[0][0]
    )
    time_stamp = models.DateTimeField()
    finalbooking_id = models.CharField(default="", max_length=50)

    def __str__(self):
        return self.payment_status






class Issue(models.Model):
    name = models.CharField(max_length=122)
    email = models.EmailField(max_length=122)
    phone = models.IntegerField()
    subject = models.CharField(max_length=122)
    userissue = models.TextField()

    def __str__(self):
        return f'{self.subject} by {self.name}'



