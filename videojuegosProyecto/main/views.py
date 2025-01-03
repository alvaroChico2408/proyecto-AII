from django.shortcuts import render
from django.http import HttpResponse
from .populateDB import populateDatabase


#muestra los títulos de las recetas que están registradas
def inicio(request):
    return render(request,'index.html')

def run_population(request):
    populateDatabase()
    return HttpResponse("Base de datos poblada exitosamente.")

