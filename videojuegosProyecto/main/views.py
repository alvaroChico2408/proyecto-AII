from django.shortcuts import render
from django.http import JsonResponse
from .populateDB import populate_database
from .models import Developer, Company, Platform, get_whoosh_index
from whoosh.index import exists_in, open_dir
import os
import shutil


#muestra los títulos de las recetas que están registradas
def inicio(request):
    return render(request,'index.html')

def database(request):
    return render(request, 'database.html')

def ejecutar_carga(request):
    try:
        
         # **Ejecutar la carga de datos en Whoosh y la BD**
        populate_database()
        
        # **Abrir el índice de Whoosh y contar los juegos indexados**
        ix = get_whoosh_index()
        with ix.searcher() as searcher:
            juegos_count = searcher.doc_count()  # Cuenta el número de documentos indexados en Whoosh
        
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
            # **Eliminar registros de la base de datos**
            Developer.objects.all().delete()
            Company.objects.all().delete()
            Platform.objects.all().delete()
            
            # **Eliminar el índice de Whoosh**
            whoosh_index_path = "whoosh_index"
            if os.path.exists(whoosh_index_path):
                shutil.rmtree(whoosh_index_path)  # Elimina el directorio del índice
                
            get_whoosh_index()

            return JsonResponse({'status': 'success', 'message': 'Base de datos e índice Whoosh eliminados correctamente'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def verificar_estado_bd(request):
    # **Verificar si hay datos en la BD**
    hay_datos_bd = Platform.objects.exists() or Developer.objects.exists() or Company.objects.exists()
    
    # **Verificar si hay datos en Whoosh**
    whoosh_index_path = "whoosh_index"
    hay_datos_whoosh = exists_in(whoosh_index_path)  # Verifica si el índice Whoosh existe

    juegos_count = 0
    if hay_datos_whoosh:
        ix = open_dir(whoosh_index_path)
        with ix.searcher() as searcher:
            juegos_count = searcher.doc_count()  # Contar cuántos documentos hay en el índice

    return JsonResponse({
        'hay_datos': hay_datos_bd or juegos_count > 0,  # Hay datos si BD o Whoosh tiene contenido
        'juegos': juegos_count,
        'plataformas': Platform.objects.count(),
        'desarrolladores': Developer.objects.count(),
        'companias': Company.objects.count(),
    })
def busqueda(request):
    return render(request, "busqueda.html")

def buscar_nombre(request):
    return render(request, "buscar_nombre.html")

from django.http import JsonResponse
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

whoosh_index_path = "whoosh_index"

def buscar_por_nombre(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse([], safe=False)  # Retorna lista vacía si no hay consulta

    try:
        # Abre el índice de Whoosh
        ix = open_dir(whoosh_index_path)
        with ix.searcher() as searcher:
            # Construye el parser para buscar en el campo "title"
            parser = QueryParser("title", ix.schema)
            query_obj = parser.parse(query)
            results = searcher.search(query_obj, limit=10)  # Máximo 10 resultados
            
            # Convertimos los resultados en una lista de diccionarios
            juegos = [
                {
                    "title": r["title"],
                    "year": r["year"],
                    "platforms": r["platforms"],
                    "developers": r["developers"],
                    "description": r["description"],
                }
                for r in results
            ]

        return JsonResponse(juegos, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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
