# messagerie/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('publier/conducteur/', views.publier_trajet_conducteur, name='publier_conducteur'),
    path('publier/passager/', views.publier_trajet_passager, name='publier_passager'),
    path('carte/', views.carte_trajets, name='carte_trajets'),
    path('publier/', views.publier_trajet, name='publier_trajet'),
    path('rechercher/', views.rechercher_trajet, name='rechercher_trajet'),
     path('api/trajets/', views.trajets_en_temps_reel, name='trajets_en_temps_reel'),
   
    # URLs pour les réservations
    path('reserver/<int:trajet_id>/', views.reserver_trajet, name='reserver_trajet'),
    path('reservation/<int:reservation_id>/gerer/', views.gerer_reservation, name='gerer_reservation'),
    path('trajet/<int:trajet_id>/annuler/', views.annuler_trajet, name='annuler_trajet'),
]
