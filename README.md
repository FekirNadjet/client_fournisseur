Pour la création et la mise à jour et la suppression d’un client, d’un fournisseur, d’une facture, d’une ligne facture on utilise les mêmes Template
-delete.html 
-update.html
-create.html 
 
– Liste Clients: 
rajouter les vues permettant de lister dans une table (avec django tables2) les clients. Pour chaque client, prévoir une colonne 'Chiffre d'affaire' qui affiche la somme des totaux de toutes les factures d'un client. Utiliser une agrégation avec la clause annotate pour rajouter cet attribut à chaque client, puis soumettre le QuerySet ainsi construit à djingo tables2.
-On ajoute dans Bill.views la calsse CleintTable 
-En suite on crée une classe ClientsView qui appelle la classe ClientsTable
-On met à jour Bill.urls on rajoutant le path vers la page qui affiche les liste des clients 
-On rajoute ensuite clients_table.html comme Template pour l’affichage de la liste des clients 
 

- Création d’un client:
prévoir un bouton qui renvoie vers un formulaire (avec crispy forms) de création d'un client
-On rajoute un bouton au niveau du Template clients_table.html qui permet de créer un nouveau client comme illustré dans l’image au-dessus 
- On définit une classe ClientCreateView dans Bill.view qui permet de crée un client
-le Template utilisé est create.html, définit dans la première partie de ce rapport

-gestion  client, liste factures d’un client: 
Rajouter une Template column avec trois boutons pour chaque client permettant de modifier et supprimer un client (formulaires avec crispy forms), et lister (avec django tables2) les factures d'un client.
a-Affichage de la liste des factures effectué par un client :
      -On définit une classe FactureTable dans Bill.views
      -on ajoute une classe ClientFactureListView  qui fait appel à FactureTable 
      -on ajoute un Template client_factures_list.html
      Et on met à jour la liste des paths dans Bill.urls
      re_path(r'^client_factures_list/(?P<pk>\d+)/$', views.ClientFacturesListView.as_view(),name='client_factures_list'),

b-modification des informations d’un client :
On crée la classe ClientUpdateView dans Bill.views :  
c-suppression d’un client :
On crée la classe ClientDeleteView dans Bill.views :
Pour les Templates utilisés comme on l’a déjà mentionné on utilise les même Template crete et delete et update 


-Ajout d’une facture, affichage total :
dans la vue qui liste les factures d'un client, prévoir un bouton qui permet d'ajouter une facture à un client (formulaire avec crispy forms), une colonne qui affiche le total de la facture. Pour afficher cette colonne, vous pouvez faire d'abord une agrégation avec la clause annotate qui rajoute le total à chaque facture, puis soumettre cette annotation comme field à django tables2.

a-création d’une facture :
-on ajoute la table FactureTable
-on crée la classe qui appelle la table FactureTable dans Bill.views
-on ajoute ensuite la classe FactureCreateView qui manipule le formulaire de création d’une facture d’un client, on met à jour la liste des urls 
 
b-affichage de la colonne total d’une facture 
on ajoute la ligne suivante à la classe ClientFacturesListView
queryset = Facture.objects.filter(client_id=self.kwargs.get('pk')).annotate(total=Sum(
    ExpressionWrapper(F('lignes__qte'), output_field=FloatField()) * F('lignes__produit__prix')))



-DateTimePicker:
pour faciliter la sélection de la date d'une facture, installer Django DateTimePickerPlus, et configurez le field date du formulaire de crétaion et modification de facture pour utiliser le Widget DateTimePickerPlus
On utilise DatePickerInput pour faciliter la creation et la modification d’une facture
form.fields['date'] = forms.DateField(
    widget=DatePickerInput(format='%m/%d/%Y')
)


-Gestion fournisseur:
Créez des vues similaires pour gérer les fournisseurs (liste dans une table, création, et template column avec boutons pour modifier et supprimer un founisseur).
-On ajoute la table FournisseurTable à bill.views
-On ajoute la classe FournisseursView qui utilise FournisseurTable our lister les fournisseur
-on ajoute les vues FournisseurUpdateView, FournisseurDeleteView et FournisseurCreateView
Ps :C’est pratiquement le même code avec les vues de manipulation la classe client 



-Table chiffre d’affaire fournisseur et client :
Table des Chiffres d'affaires par fournisseur (utiliser la clause annotate combinée avec la clause values).
Table des chiffres d'affaires par client dans l'ordre décroissant du chiffre d'affaire (utiliser les clauses annotate, values et order_by).
-on ajoute les tables CaClientTable pour les client et CAfournisseurTable our les fournisseurs
-on définit une classe Dashboardtables qui utilise les deux tables précédentes, pour la table des clients on fait un affichage décroissant  des chiffres d’affaire avec order_by
 
 
-Courbe chiffre affaire réparti par catégorie:
Une courbe de type Radar (toujours avec Django jchart) qui affiche le chiffre d'affaire réparti par catégorie de Produit. Pour ce faire, il faudra enrichir le modèle avec la classe Catégorie (alimentation, habillement, meuble, electromenager, IT, etc.) et modifier Produit pour que chaque produit désigne sa catégorie. faire une migration du modèle. Pour afficher le radar, pensez à utiliser une agrégation (clause values sur categorie combinée avec la clause annotate pour calculer le chiffre d'affaire par catégorie)
-ajout de lu model Category dans bill.models
-modification du model Produit en rajoutant un Field comme clé étrangère à la classe category 
  
  
-Lignes facture :
a-modification, création et la supression d’une ligne facture :
Pour la modification et la création et la suppression  d’une ligne facture on a crée les vues suivantes ayant un code similaire à la manipulation des factures d’un client donné.
-LigneFactureCreateView
-LigneFactureUpdateView
-LigneFactureDeleteView
b-Liste des lignes facture d’une facture
 création de la table LigneFactureTable, utilisé dans la vue FactureDetail View pour l’affichage de la liste des lignes facture d’une facture choisit


Templates :
a-Dashboard
Dashboard qui contient la liste des chiffres d’affaire des clients et fournisseur ainsi qu’un menu vers les différentes pages : 
-liste clients
-liste fournisseurs
-liste factures
http://127.0.0.1:8000/bill/dashboard/
 
b-Liste Clients, Liste fournisseur, liste factures
une table qui contient les informations de chaque client ainsi que le chiffre d’affaire de chaque client,
-un bouton pour la suppression d’un client 
-un bouton pour la modification d’un client 
-un bouton pour lister les factures d’un client donnée
-un bouton pour l’ajout d’un client 
http://127.0.0.1:8000/bill/clients_table/
 
 
f-Ajout et modification d’un client, fournisseur, facture, ligne facture
la page contient un formulaire pour la création d’un client, celle de la modification d’un client est similaire à la suivante
les pages ajout et modification d’un fournisseur, facture et ligne facture comportent aussi pratiquement les mêmes infos
http://127.0.0.1:8000/bill/client_create/
 
