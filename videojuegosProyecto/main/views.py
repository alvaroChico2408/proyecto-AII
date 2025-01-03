from django.shortcuts import render
from django.http import JsonResponse
from .populateDB import populate_database
from .models import Developer, Company, Platform, VideoGame


#muestra los títulos de las recetas que están registradas
def inicio(request):
    return render(request,'index.html')

def database(request):
    return render(request, 'database.html')

def ejecutar_carga(request):
    try:
        populate_database()
         # Contar los registros insertados en cada tabla
        juegos_count = VideoGame.objects.count()
        plataformas_count = Platform.objects.count()
        desarrolladores_count = Developer.objects.count()
        companias_count = Company.objects.count()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Base de datos cargada correctamente',
            'juegos': juegos_count,
            'plataformas': plataformas_count,
            'desarrolladores': desarrolladores_count,
            'companias': companias_count
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def eliminar_database(request):
    if request.method == "POST":
        try:
            Developer.objects.all().delete()
            Company.objects.all().delete()
            Platform.objects.all().delete()
            VideoGame.objects.all().delete()
            return JsonResponse({'status': 'success', 'message': 'Base de datos eliminada correctamente'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

