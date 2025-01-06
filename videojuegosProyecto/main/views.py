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

def verificar_estado_bd(request):
    hay_datos = VideoGame.objects.exists() or Platform.objects.exists() or Developer.objects.exists() or Company.objects.exists()

    return JsonResponse({
        'hay_datos': hay_datos,
        'juegos': VideoGame.objects.count(),
        'plataformas': Platform.objects.count(),
        'desarrolladores': Developer.objects.count(),
        'companias': Company.objects.count(),
    })

def busqueda(request):
    return render(request, "busqueda.html")

def buscar_nombre(request):
    return render(request, "buscar_nombre.html")

def buscar_por_nombre(request):
    query = request.GET.get("q", "")

    if query:
        juegos = VideoGame.objects.filter(title__icontains=query).values(
            "title", "year", "platforms", "developers", "description"
        )
        return JsonResponse(list(juegos), safe=False)
    
    return JsonResponse([], safe=False)

def buscar_plataforma(request):
    return render(request, "buscar_plataforma.html")

def buscar_desarrollador(request):
    return render(request, "buscar_desarrollador.html")

def buscar_compania(request):
    return render(request, "buscar_compania.html")

def obtener_companias(request):
    companias = list(Company.objects.values_list('name', flat=True).distinct())
    return JsonResponse(companias, safe=False)

def buscar_por_compania(request):
    compania = request.GET.get('q', '')

    if not compania:
        return JsonResponse([], safe=False)

    juegos = VideoGame.objects.filter(companies__icontains=compania).values(
        'title', 'year', 'platforms', 'developers', 'opinion'
    )

    return JsonResponse(list(juegos), safe=False)
