from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import animales_view, crear_animal_view, editar_animal_view, eliminar_animal_view, crear_vacuna_view, logout_view  # Importar la vista personalizada

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),  # Usar la vista personalizada para logout
    path('registro/', views.registro_view, name='registro'),
    path('acerca-de-nosotros/', views.acerca_de_nosotros, name='acerca_de_nosotros'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('lotes/', views.lotes_view, name='lotes'),
    path('animales/', animales_view, name='animales'),
    path('vacunas/', views.vacunas_view, name='vacunas'),
    path('lotes/asignar/<int:lot_id>/', views.lotes_view, name='asignar_animales'),
    path('lotes/crear/', views.crear_lote_view, name='crear_lote'),
    path('lotes/eliminar/<int:lot_id>/', views.eliminar_lote_view, name='eliminar_lote'),
    path('animales/crear/', crear_animal_view, name='crear_animal'),
    path('animales/editar/<int:animal_id>/', editar_animal_view, name='editar_animal'),
    path('animales/eliminar/<int:animal_id>/', eliminar_animal_view, name='eliminar_animal'),
    path('vacunas/crear/', crear_vacuna_view, name='crear_vacuna'),
]