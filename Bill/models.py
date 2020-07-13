from django.db import models
from django import utils
import datetime

# Create your models here.



class Client(models.Model):
    SEXE = (
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=10, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXE)

    def __str__(self):
        return self.nom + ' ' + self.prenom


class Fournisseur(models.Model):

    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nom + ' ' + self.prenom

class Category(models.Model):
    nom= models.CharField(max_length=120)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    designation = models.CharField(max_length=50)
    prix = models.FloatField(default=0)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='products')
    def __str__(self):
        return self.designation


class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(default=utils.timezone.now)

    def total(self):
        total = 0.0
        for i in self.lignes.all():
            total += i.qte * i.produit.prix
        return total


class LigneFacture(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE,related_name='facture')
    qte = models.IntegerField(default=1)
    facture = models.ForeignKey(
        Facture, on_delete=models.CASCADE, related_name='lignes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['produit', 'facture'], name="produit-facture")
        ]

