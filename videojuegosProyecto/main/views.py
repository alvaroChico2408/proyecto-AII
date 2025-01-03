from django.shortcuts import render
from django.http import JsonResponse
from .populateDB import populate_database


#muestra los títulos de las recetas que están registradas
def inicio(request):
    return render(request,'index.html')

def database(request):
    return render(request, 'database.html')

def ejecutar_carga(request):
    print("hola")
    try:
        populate_database()  # Llamamos a la función que popula la base de datos
        print("hola2")
        return JsonResponse({'status': 'success', 'message': 'Base de datos cargada correctamente'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

