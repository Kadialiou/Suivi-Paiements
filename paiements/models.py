from django.db import models
from django.utils import timezone

class ClientPaiement(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    montant_demande = models.DecimalField(max_digits=10, decimal_places=2)
    montant_verse = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField(default=timezone.now)

    @property
    def solde(self):
        return self.montant_demande - self.montant_verse

    @property
    def statut(self):
        if self.solde == 0:
            return "✅ Payé"
        elif self.solde < 0:
            return "⚠️ Trop versé"
        else:
            return "❌ Incomplet"

    def __str__(self):
        return f"{self.nom} {self.prenom}"
