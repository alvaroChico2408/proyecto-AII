from django.shortcuts import render
from django.http import JsonResponse
from .populateDB import populate_database
from .models import Developer, Company, Platform, get_whoosh_index
from whoosh.index import exists_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.query import Wildcard
from .recommendations import ContentRecommender
import os
import shutil

whoosh_index_path = "whoosh_index"

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

def buscar_por_nombre(request):
    query = request.GET.get("q", "").strip().lower()  # Obtiene y normaliza la consulta

    if not query:
        return JsonResponse([], safe=False)  # Si no hay consulta, devuelve lista vacía

    try:
        ix = open_dir(whoosh_index_path)  # Abre el índice de Whoosh
        with ix.searcher() as searcher:
            # Usamos `Wildcard` para buscar cualquier palabra que contenga la consulta
            query_obj = Wildcard("title", f"*{query}*")  

            print(f"Consulta Whoosh: {query_obj}")  # Depuración

            results = searcher.search(query_obj)  # Busca hasta 20 resultados
            
            juegos = [
                {
                    "title": r["title"],
                    "year": r["year"],
                    "platforms": r["platforms"],
                    "developers": r["developers"],
                    "companies": r["companies"],
                    "description": r["description"],
                }
                for r in results
            ]

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(juegos, safe=False)  # Devuelve los resultados en formato JSON

def buscar_plataforma(request):
    return render(request, "buscar_plataforma.html")

def obtener_plataformas(request):
    plataformas = list(Platform.objects.values_list('name', flat=True).distinct())
    return JsonResponse(plataformas, safe=False)

def buscar_por_plataforma(request):
    plataforma = request.GET.get("q", "").strip()  # Obtiene el parámetro de búsqueda

    if not plataforma:
        return JsonResponse([], safe=False)  # Si no hay consulta, devuelve una lista vacía

    try:
        ix = open_dir(whoosh_index_path)  # Abre el índice de Whoosh
        with ix.searcher() as searcher:
            # Se usa el campo "platforms" en lugar de "developers"
            query = QueryParser("platforms", ix.schema).parse(f'"{plataforma}"')
            print(f"Consulta Whoosh: {query}")

            results = searcher.search(query, limit=None)  # Busca sin límite de resultados
            
            juegos = [
                {
                    "title": r["title"],
                    "year": r["year"],
                    "platforms": r["platforms"],
                    "developers": r["developers"],
                    "companies": r["companies"],  # Ahora correctamente referenciado
                    "opinion": r["description"],  # Mapea la descripción correctamente
                }
                for r in results
            ]

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(juegos, safe=False)



def buscar_desarrollador(request):
    return render(request, "buscar_desarrollador.html")

def obtener_desarrolladores(request):
    desarrolladores = list(Developer.objects.values_list('name', flat=True).distinct())
    return JsonResponse(desarrolladores, safe=False)

def buscar_por_desarrollador(request):
    desarrollador = request.GET.get("q", "").strip()  # Obtiene el parámetro de búsqueda

    if not desarrollador:
        return JsonResponse([], safe=False)  # Si no hay consulta, devuelve una lista vacía

    try:
        ix = open_dir(whoosh_index_path)  # Abre el índice de Whoosh
        with ix.searcher() as searcher:
            # Se usa el campo "developers" en lugar de "companies"
            query = QueryParser("developers", ix.schema).parse(f'"{desarrollador}"')
            print(f"Consulta Whoosh: {query}")

            results = searcher.search(query, limit=None)  # Busca sin límite de resultados
            
            juegos = [
                {
                    "title": r["title"],
                    "year": r["year"],
                    "platforms": r["platforms"],
                    "developers": r["developers"],
                    "companies": r["companies"],  # Ahora correctamente referenciado
                    "opinion": r["description"],  # Mapea la descripción correctamente
                }
                for r in results
            ]

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(juegos, safe=False)

def buscar_compania(request):
    return render(request, "buscar_compania.html")

def obtener_companias(request):
    companias = list(Company.objects.values_list('name', flat=True).distinct())
    return JsonResponse(companias, safe=False)

def buscar_por_compania(request):
    compania = request.GET.get("q", "").strip()  # Obtiene el parámetro de búsqueda

    if not compania:
        return JsonResponse([], safe=False)  # Si no hay consulta, devuelve una lista vacía

    try:
        ix = open_dir(whoosh_index_path)  # Abre el índice de Whoosh
        with ix.searcher() as searcher:
            query = QueryParser("companies", ix.schema).parse(f'"{compania}"')
            print(f"Consulta Whoosh: {query}")
            results = searcher.search(query, limit=None)  # Busca sin límite de resultados
            
            juegos = [
                {
                    "title": r["title"],
                    "year": r["year"],
                    "platforms": r["platforms"],
                    "developers": r["developers"],
                    "companies": r['companies'],
                    "opinion": r["description"],  # Mapea la descripción correctamente
                }
                for r in results
            ]
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(juegos, safe=False)  # Devuelve los resultados en formato JSON

def recomendaciones(request):
    return render(request, "recomendaciones.html")

def obtener_recomendaciones(request):
    juego_base = request.GET.get("title", "").strip()

    if not juego_base:
        return JsonResponse([], safe=False)

    try:
        # **Inicializamos el recomendador**
        recommender = ContentRecommender()
        
        # **Obtenemos las recomendaciones basadas en contenido**
        recomendaciones = recommender.getRecommendedItems(juego_base)

        # **Preparamos la respuesta con información detallada**
        juegos_recomendados = []
        ix = open_dir(whoosh_index_path)
        with ix.searcher() as searcher:
            for juego in recomendaciones:
                query = QueryParser("title", ix.schema).parse(f'"{juego["title"]}"')
                result = searcher.search(query, limit=1)

                if result:
                    r = result[0]
                    juegos_recomendados.append({
                        "title": r["title"],
                        "year": r["year"],
                        "platforms": r["platforms"],
                        "developers": r["developers"],
                        "companies": r["companies"],
                        "description": r["description"],
                        "similitud": juego["similitud"],  # Ya está en porcentaje
                    })

        return JsonResponse(juegos_recomendados, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)