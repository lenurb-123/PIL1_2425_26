from django.urls import path
from . import views

urlpatterns = [
    # Liste des utilisateurs disponibles pour discuter
    path('discussions/utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),

    # Démarrer une discussion avec un utilisateur précis
    path('discussions/<int:user_id>/', views.demarrer_discussion, name='demarrer_discussion'),

    # Vue de la conversation avec un utilisateur
    path('conversation/<int:discussion_id>/', views.conversation, name='conversation'),

    path('discussions/', views.liste_discussions, name='liste_discussions'),
    path('nouvelle/', views.nouvelle_conversation, name='nouvelle_conversation'),
    path('groupe/creer/', views.creer_groupe, name='creer_groupe'),
    path('groupe/<int:groupe_id>/', views.groupe_conversation, name='groupe_conversation'),
    path('demarrer/<int:user_id>/', views.demarrer_discussion, name='demarrer_discussion'),
    path('recherche-utilisateurs/', views.recherche_utilisateurs, name='recherche_utilisateurs'),
    path('historique/<int:discussion_id>/', views.historique_discussion, name='historique_discussion'),
]
