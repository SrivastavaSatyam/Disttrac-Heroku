from django.contrib import admin
from django.urls import path 
from measurement import views

app_name='measurement'

urlpatterns = [
    path('',views.calculate_dis, name='calculate-view')
]
