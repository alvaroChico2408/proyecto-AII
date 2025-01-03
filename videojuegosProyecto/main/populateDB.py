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
    # Crear sets para almacenar plataformas, desarrolladores y compañías sin duplicados
    desarrolladores_set = set()
    companias_set = set()
    plataformas_set = set()
    
    for p in range(1,PAGINAS+1):
        url="https://playthatgame.co.uk/?action=biglist&num="+str(p)
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f,"lxml")      
        filas = s.find("table", class_=["biglist"]).find_all("tr")
        
        

        #Cada fila tiene dos columnas
        for fila in filas:
            
            # Obtener cada una de las columnas
            columnas = fila.find_all("td")

            for columna in columnas:  # recorrer las dos columnas
                
                #Vaciamos las listas
                desarrolladores_lista = []
                companias_lista = []
                plataformas_lista = []
                
                #Extraer el título quitándole el #)
                titulo = columna.find("div", class_="gamename")
                if titulo:
                    titulo = re.sub(r"^\d+\)\s*", "", titulo.text.strip())
                else:
                    titulo = "Desconocido"
                
                #Extraer el año
                #Es el siguiente al texto que pone "year of release"
                year = columna.find(text=lambda x: x and "Year of Release:" in x)
                year = year.next.strip() if year else "Desconocido"
                
                # Extraer la descripción
                # Está después del último br de cada td, si hay un be, está después el penúltimo br y después del primer be
                brs = columna.find_all("br")
                    
                # Encontrar todos los <be> en la columna
                bes = columna.find_all("be")
                
                # Si hay be
                if bes:  
                    be_tag = bes[0]
                    #Está después del penúltimo br 
                    opinion = brs[-2].next.strip() if brs else "Desconocido"
                    # Y después del 1 be
                    opinion = opinion + be_tag.next.strip() if be_tag.next else "Descripción no encontrada"
                else:
                    #Si no está después de penúltimo br
                    opinion = brs[-1].next.strip() if brs else "Desconocido"
                    
                # Extraer desarrolladores
                #Está después del texto de Developed By:. Separamos por comas y metemos en la lista
                desarrolladores = columna.find(text=lambda x: x and "Developed By:" in x)
                desarrolladores_lista = [dev.strip() for dev in desarrolladores.next.strip().split(",")] if desarrolladores else []
                #Separamos la lista por comas en caso de que hubiera más de un elemento, y generamos el string
                desarrolladores_string = ", ".join(desarrolladores_lista)
                #Insertamos en el set
                desarrolladores_set.update(desarrolladores_lista)
                
                # Extraer companias
                # Está después del texto de Developed By:. Separamos por comas y metemos en la lista
                companias = columna.find(text=lambda x: x and "Published By:" in x)
                companias_lista = [pub.strip() for pub in companias.next.strip().split(",")] if companias else []
                #Separamos la lista por comas en caso de que hubiera más de un elemento, y generamos el string
                companias_string = ", ".join(companias_lista)
                #Insertamos en el set
                companias_set.update(companias_lista)
                
                # Extraer plataformas
                # Está después del texto de Platforms:. Separamos por comas y metemos en la lista
                plataformas = columna.find(text=lambda x: x and ("Platforms:" in x or "Platform:" in x))
                plataformas_lista = [plat.strip() for plat in plataformas.next.strip().split(",")] if plataformas else []
                #Separamos la lista por comas en caso de que hubiera más de un elemento, y generamos el string
                plataformas_string = ", ".join(plataformas_lista)  
                #Insertamos en el set
                plataformas_set.update(plataformas_lista)
                
                # **Guardar VideoGame en la base de datos**
                video_game, created = VideoGame.objects.get_or_create(
                    title=titulo,
                    year=year,
                    description=opinion,
                    developers=desarrolladores_string,
                    companies=companias_string,
                    platforms=plataformas_string
                )
                print(f"Guardado: {video_game.title}")
    # **Guardar desarrolladores, compañías y plataformas sin duplicados**
    for dev in desarrolladores_set:
        Developer.objects.get_or_create(name=dev)

    for comp in companias_set:
        Company.objects.get_or_create(name=comp)

    for plat in plataformas_set:
        Platform.objects.get_or_create(name=plat)
        
    print("Todos los datos han sido almacenados correctamente.")
                
    return True

