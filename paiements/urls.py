from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('login/', views.connexion, name='login'),
    path('logout/', views.deconnexion, name='logout'),
    path('', views.liste_paiements, name='liste_paiements'),
    path('ajouter/', views.ajouter_paiement, name='ajouter_paiement'),
    path('modifier/<int:paiement_id>/', views.modifier_paiement, name='modifier_paiement'),
    path('supprimer/<int:paiement_id>/', views.supprimer_paiement, name='supprimer_paiement'),
    path('reinitialiser/', views.reinitialiser_paiements, name='reinitialiser_paiements'),
    path('export/excel/', views.export_excel, name='export_excel'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]
