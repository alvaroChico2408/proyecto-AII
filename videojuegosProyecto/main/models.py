from django.db import models

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


class VideoGame(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    
    developers = models.CharField(max_length=500, blank=True)  # Guardará nombres separados por comas
    companies = models.CharField(max_length=500, blank=True)   # Guardará nombres separados por comas
    platforms = models.CharField(max_length=500, blank=True)   # Guardará nombres separados por comas

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title', )
