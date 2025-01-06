from whoosh.index import open_dir
from whoosh.qparser import QueryParser

WHOOSH_INDEX_DIR = "whoosh_index"  # Ruta del índice

def buscar_undertale():
    ix = open_dir(WHOOSH_INDEX_DIR)
    with ix.searcher() as searcher:
        query = QueryParser("title", ix.schema).parse("Undertale")
        results = searcher.search(query)
        for hit in results:
            print(hit)

buscar_undertale()

