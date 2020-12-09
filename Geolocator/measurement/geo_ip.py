from django.contrib.gis.geoip2 import GeoIP2


#HElpper Fiunction 

def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon

def cords(latA,lonA,latB=None,lonB=None):
    crd= (latA,lonA)    
    if latB:
        crd=[(latA+latB)/2 ,(lonA+lonB)/2]
        
    return crd   

def zooming(distance):
    if distance<=1000:
        return 10
    elif distance>100 and distance<=5000:
        return 5
    else:
        return 2            