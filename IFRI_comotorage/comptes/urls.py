from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='accueil'),
    path('recherche-utilisateur/', views.recherche_utilisateur, name='recherche_utilisateur'),
    path('inscription/', views.inscription, name='inscription'),
    path('infos/', views.infos, name='infos'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.logout_view, name='deconnexion'),
    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),  # ✅ vue protégée
    path('profil/', views.profil, name='profil'),
    path('parametres/', views.parametres, name='parametres'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='comptes/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='comptes/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='comptes/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='comptes/password_reset_complete.html'), name='password_reset_complete'),
    path('notifications/',views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/marquer-lue/', views.marquer_notification_lue, name='marquer_notification_lue'),
    path('newsletter/inscription/', views.newsletter_inscription, name='newsletter_inscription'),
    path('contact/', views.contact, name='contact'),
    path('api/conversations/', views.get_conversations, name='get_conversations'),
    path('api/conversations/<int:conversation_id>/messages/', views.get_messages, name='get_messages'),
    path('api/conversations/<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('api/conversations/create/', views.create_conversation, name='create_conversation'),
    path('mes-trajets/', views.mes_trajets, name='mes_trajets'),
    path('discussions/', views.discussions, name='discussions'),
    path('notifications/supprimer-toutes/', views.supprimer_toutes_notifications, name='supprimer_toutes_notifications'),
    path('payment/', views.payment, name='payment'),
    
    # URL de debug
    path('debug/notifications/', views.debug_notifications, name='debug_notifications'),
    
    # URLs pour l'authentification à deux facteurs
    path('2fa/setup/', views.setup_2fa, name='setup_2fa'),
    path('2fa/verify/', views.verify_2fa, name='verify_2fa'),
    path('2fa/disable/', views.disable_2fa, name='disable_2fa'),
]
# Note: The 'liste_utilisateurs' view is protected by the @login_required decorator,