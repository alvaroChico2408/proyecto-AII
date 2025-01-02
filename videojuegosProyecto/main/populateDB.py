from .models import Developer, Company, Platform, VideoGame
from bs4 import BeautifulSoup
import urllib.request
import re

# lineas para evitar error SSL
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
    
PAGINAS= 5


def populateDatabase():
    
    #borrar tablas
    Developer.objects.all().delete()
    Company.objects.all().delete()
    Platform.objects.all().delete()
    VideoGame.objects.all().delete()
    
    lista=[]
    
    for p in range(1,PAGINAS+1):
        url="https://playthatgame.co.uk/?action=biglist&num="+str(p)
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f,"lxml")      
        print("hola")
        juegos = s.ol.find_all("div", class_= "product-item-details")
        print("hola")
        
    return lista

