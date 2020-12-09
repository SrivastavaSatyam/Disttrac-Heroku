from django.shortcuts import render,HttpResponse,get_object_or_404
#manually
from measurement.models import Mes
from datetime import datetime
from measurement.form import MeasurementModelForm
from geopy.geocoders import Nominatim
from measurement.geo_ip import get_geo , cords , zooming
from geopy.distance import geodesic 
import geocoder
import folium 
from django.contrib import messages


# Create your views here.


def calculate_dis(request):

    distance=None


    form=MeasurementModelForm(request.POST or None)
    geolocator =Nominatim(user_agent="measurement")

    trak= geocoder.ip('me')
    ip=trak.ip
    # ip='47.30.209.199'
    country, city, lat, long = get_geo(ip)
    # print("country",country)
    # print(f"Location {city['city']}, {city['region']}, {city['country_name']}, {city['country_code']}" )
    # print("city",)
    # print('country_code',)
    # print('region',)
    # print("lat",lat)
    # print("lon",long)
    l_lat=lat
    l_long=long
    pointa=(l_lat, l_long)

    map=folium.Map(location=(l_lat, l_long))
    folium.Marker(location=[l_lat, l_long],raduis=5,tooltip=f"{city['city']}, {city['region']}, {city['country_name']}, {city['country_code']}",icon=folium.Icon(color="red")).add_to(map)
    folium.TileLayer('Mapbox Control Room').add_to(map)
    folium.TileLayer('Stamen Toner').add_to(map)
    folium.TileLayer('Stamen Terrain').add_to(map)
    folium.TileLayer('Stamen Watercolor').add_to(map)
    folium.TileLayer('CartoDB positron').add_to(map)
    folium.TileLayer('CartoDB dark_matter').add_to(map)




    if form.is_valid(): 

        instance = form.save(commit=False)
        
        locat=form.cleaned_data.get('Location')
        location=geolocator.geocode(locat)
        # print(location) 
        l_lat=location.latitude
        l_long=location.longitude
        pointa=(l_lat, l_long)

        map=folium.Map(location=(l_lat, l_long))
        folium.Marker(location=[l_lat, l_long],raduis=5,tooltip=f"{city['city']}, {city['region']}, {city['country_name']}, {city['country_code']}",icon=folium.Icon(color="red")).add_to(map)
        folium.TileLayer('Mapbox Control Room').add_to(map)
        folium.TileLayer('Stamen Toner').add_to(map)
        folium.TileLayer('Stamen Terrain').add_to(map)
        folium.TileLayer('Stamen Watercolor').add_to(map)
        folium.TileLayer('CartoDB positron').add_to(map)
        folium.TileLayer('CartoDB dark_matter').add_to(map)


        # print("##",location) 
        


        dest = form.cleaned_data.get('Destination')
        destination=geolocator.geocode(dest)
        # print("Destination",destination)
        if destination==None:
            messages.error(request,"Check the Destination Location then Try Again")
        else:

            d_lat=destination.latitude
            d_lon=destination.longitude
            pointb=(d_lat,d_lon)
            distance=round(geodesic(pointa, pointb).km,2)        

            map=folium.Map(location=cords(l_lat,l_long,d_lat,d_lon),zoom_start=zooming(distance))

            folium.Marker(location=[l_lat, l_long],raduis=5,tooltip=f"{city['city']}, {city['region']}, {city['country_name']}, {city['country_code']}",icon=folium.Icon(color="red")).add_to(map)
            folium.Marker(location=[d_lat, d_lon],raduis=5,tooltip=dest,icon=folium.Icon(color="blue")).add_to(map)
            folium.TileLayer('Mapbox Control Room').add_to(map)
            folium.TileLayer('Stamen Toner').add_to(map)
            folium.TileLayer('Stamen Terrain').add_to(map)
            folium.TileLayer('Stamen Watercolor').add_to(map)
            folium.TileLayer('CartoDB positron').add_to(map)
            folium.TileLayer('CartoDB dark_matter').add_to(map)

            folium.PolyLine(locations=(pointa, pointb), weight=5,tooltip=f"Distance is {distance}km",color='blue').add_to(map)
            
            instance.Location=location
            instance.Distance= distance
            instance.save()

        
    map.add_child(folium.LayerControl())
    map=map._repr_html_()

    context={
        # 'distane_obj':obj,
        'Distance':Mes.objects.last(),
        'form':form,
        'map':map,
    }


    return render(request,'index.html',context)
