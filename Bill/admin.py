from django.contrib import admin
from Bill.models import Client, Produit, Facture, LigneFacture, Fournisseur, Category

# Register your models here.
admin.site.register(Client)
admin.site.register(Facture)
admin.site.register(Produit)
admin.site.register(LigneFacture)
admin.site.register(Fournisseur)
admin.site.register(Category)
