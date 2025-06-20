# Generated by Django 5.1.7 on 2025-06-18 20:34

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trajet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conducteur_nom', models.CharField(default='', max_length=100)),
                ('conducteur_prenom', models.CharField(default='', max_length=100)),
                ('depart', models.CharField(default='', max_length=255)),
                ('arrivee', models.CharField(default='', max_length=255)),
                ('heure_depart', models.DateTimeField(default=django.utils.timezone.now)),
                ('heure_arrivee', models.DateTimeField(default=django.utils.timezone.now)),
                ('places_disponibles', models.PositiveIntegerField(default=1)),
                ('tarif', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='PositionUtilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('utilisateur', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passager_nom', models.CharField(default='', max_length=100)),
                ('passager_prenom', models.CharField(default='', max_length=100)),
                ('depart', models.CharField(default='', max_length=255)),
                ('arrivee', models.CharField(default='', max_length=255)),
                ('heure_depart', models.DateTimeField(default=django.utils.timezone.now)),
                ('heure_arrivee', models.DateTimeField(default=django.utils.timezone.now)),
                ('places_reservees', models.PositiveIntegerField(default=1)),
                ('date_reservation', models.DateTimeField(auto_now_add=True)),
                ('created_le', models.DateTimeField(auto_now_add=True)),
                ('trajet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='trajets.trajet')),
            ],
        ),
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('commentaire', models.TextField(blank=True)),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avis_donnes', to=settings.AUTH_USER_MODEL)),
                ('destinataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avis_recus', to=settings.AUTH_USER_MODEL)),
                ('trajet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avis', to='trajets.trajet')),
            ],
        ),
        migrations.CreateModel(
            name='TrajetPassage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lieu_depart', models.CharField(max_length=255)),
                ('lieu_arrivee', models.CharField(default='IFRI UAC Bénin', max_length=255)),
                ('heure_souhaitee', models.TimeField(blank=True, null=True)),
                ('jours_semaine', models.CharField(max_length=50)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('statut', models.CharField(choices=[('proposé', 'Proposé'), ('accepté', 'Accepté'), ('terminé', 'Terminé'), ('annulé', 'Annulé')], default='proposé', max_length=20)),
                ('tarif', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('passager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrajetTaxi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lieu_depart', models.CharField(default='', max_length=255)),
                ('lieu_arrivee', models.CharField(default='', max_length=255)),
                ('heure_depart', models.TimeField(blank=True, null=True)),
                ('jours_semaine', models.CharField(default='', max_length=50)),
                ('places_disponibles', models.PositiveIntegerField(default=1)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('statut', models.CharField(choices=[('proposé', 'Proposé'), ('accepté', 'Accepté'), ('terminé', 'Terminé'), ('annulé', 'Annulé')], default='proposé', max_length=20)),
                ('tarif', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('conducteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
