import os
import numpy as np
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

whoosh_index_path = "whoosh_index"  # Ruta del índice de Whoosh

class ContentRecommender:
    def __init__(self):
        """Inicializa la clase y carga los datos de Whoosh."""
        self.prefs = self.load_data()
    
    def load_data(self):
        """Carga los datos del índice Whoosh y los organiza para calcular similitudes."""
        prefs = {}
        ix = open_dir(whoosh_index_path)
        with ix.searcher() as searcher:
            query = QueryParser("title", ix.schema).parse("*")
            results = searcher.search(query, limit=None)

            for r in results:
                prefs[r["title"]] = {
                    "title": r["title"].lower(),
                    "platforms": r["platforms"].lower(),
                    "developers": r["developers"].lower(),
                    "companies": r["companies"].lower(),
                    "description": r["description"].lower(),
                }
        return prefs

    def calcular_similitud_texto(self, texto1, texto2):
        """Calcula la similitud de coseno entre dos textos usando TF-IDF."""
        vectorizer = TfidfVectorizer().fit_transform([texto1, texto2])
        similarity_matrix = cosine_similarity(vectorizer)
        return similarity_matrix[0, 1]  # Similaridad entre los dos textos

    def topMatches(self, item, n=10):
        """Encuentra los juegos más similares basados en contenido."""
        if item not in self.prefs:
            return []

        juego_base = self.prefs[item]
        juegos_similares = []

        for otro_juego, datos in self.prefs.items():
            if otro_juego == item:
                continue

            # Calculamos las similitudes individuales
            similitud_titulo = self.calcular_similitud_texto(juego_base["title"], datos["title"])
            similitud_companias = self.calcular_similitud_texto(juego_base["companies"], datos["companies"])
            similitud_desarrolladores = self.calcular_similitud_texto(juego_base["developers"], datos["developers"])
            similitud_plataformas = self.calcular_similitud_texto(juego_base["platforms"], datos["platforms"])
            similitud_opinion = self.calcular_similitud_texto(juego_base["description"], datos["description"])

            # Ponderación de las similitudes (ajustable según importancia)
            puntuacion_final = (0.4 * similitud_titulo +
                                0.15 * similitud_companias +
                                0.1 * similitud_desarrolladores +
                                0.05 * similitud_plataformas +
                                0.3 * similitud_opinion)

            juegos_similares.append({
                "title": datos["title"],
                "platforms": datos["platforms"],
                "developers": datos["developers"],
                "companies": datos["companies"],
                "description": datos["description"],
                "similitud": round(puntuacion_final * 100, 2)  # Convertimos en porcentaje
            })

        juegos_similares = sorted(juegos_similares, key=lambda x: x["similitud"], reverse=True)
        return juegos_similares[:n]

    def getRecommendedItems(self, item):
        """Obtiene las recomendaciones más similares."""
        return self.topMatches(item, n=10)
