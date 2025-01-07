"""
URL configuration for videojuegosProyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.inicio),
    path('cargarBaseDatos/', views.database),
    path('ejecutarCarga/', views.ejecutar_carga),
    path('eliminarBaseDatos/',views.eliminar_database),
    path('verificarEstadoBD/', views.verificar_estado_bd, name='verificarEstadoBD'),
    path("busqueda/", views.busqueda),
    path("busqueda/nombre/", views.buscar_nombre),
    path("busqueda/plataforma/", views.buscar_plataforma),
    path("busqueda/desarrollador/", views.buscar_desarrollador),
    path("busqueda/compania/", views.buscar_compania),
    path("buscarPorNombre/", views.buscar_por_nombre),
    path("obtener_companias/", views.obtener_companias),
    path("buscarPorCompania/", views.buscar_por_compania),
    path("obtener_desarrolladores/", views.obtener_desarrolladores),
    path("buscarPorDesarrollador/", views.buscar_por_desarrollador),
]
