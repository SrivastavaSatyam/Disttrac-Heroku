from django.db import models
from measurement.geo_ip import get_geo
import geocoder
from django import forms

# Create your models here.
trak= geocoder.ip('me')
ip=trak.ip
# ip='47.30.209.199'
country, city, lat, long = get_geo(ip)

class Mes(models.Model):
    Location=models.CharField(max_length=200,default=city['city'])
    Destination=models.CharField(max_length=200 )
    Distance=models.DecimalField(max_digits=10, decimal_places=2)
    Date=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Distance from {self.Location.upper()} to {self.Destination.upper()} is {self.Distance} km "
    