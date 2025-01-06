from django.db import models
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.qparser import QueryParser
import os

# **Directorio donde se almacenará el índice de Whoosh**
INDEX_DIR = "whoosh_index"

# **Esquema de Whoosh para indexar videojuegos**
schema = Schema(
    title=TEXT(stored=True),
    year=NUMERIC(stored=True),
    platforms=TEXT(stored=True),
    developers=TEXT(stored=True),
    companies=TEXT(stored=True),
    description=TEXT(stored=True)
)

# **Función para obtener o crear el índice Whoosh**
def get_whoosh_index():
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
        return create_in(INDEX_DIR, schema=schema)
    return open_dir(INDEX_DIR)

class Developer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class Platform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
