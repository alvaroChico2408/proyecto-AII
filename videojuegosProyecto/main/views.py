from django.shortcuts import render
from django.http import HttpResponse
from .populateDB import populate_database


#muestra los títulos de las recetas que están registradas
def inicio(request):
    return render(request,'index.html')

def database(request):
    return render(request, 'database.html')

