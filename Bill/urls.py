from django.urls import path, re_path, include
from Bill import views
urlpatterns = [
    re_path(r'^facture_detail/(?P<pk>\d+)/$',
            views.facture_detail_view, name='facture_detail'),
    re_path(r'^clients_table/$', views.ClientsView.as_view(),
            name='clients_table'),
    re_path(r'^update_client/(?P<pk>\d+)/$', views.ClientUpdateView.as_view(),
            name='client_update'),
    re_path(r'^delete_client/(?P<pk>\d+)/$', views.ClientDeleteView.as_view(),
            name='client_delete'),
    re_path(r'^client_factures_list/(?P<pk>\d+)/$', views.ClientFacturesListView.as_view(),
            name='client_factures_list'),
    re_path(r'^client_create/$', views.ClientCreateView.as_view(),
            name='client_create'),
    re_path(r'^facture_create/(?P<client_pk>\d+)/$', views.FactureCreateView.as_view(),
            name='facture_create'),

    re_path(r'^fournisseur_table/$', views.FournisseursView.as_view(),
            name='fournisseur_table'),
    re_path(r'^fournisseur_delete/(?P<pk>\d+)/$', views.FournisseurDeleteView.as_view(), name='fournisseur_delete'),

    re_path(r'^fournisseur_update/(?P<pk>\d+)/$', views.FournisseurUpdateView.as_view(),
            name='fournisseur_update'),
    re_path(r'^fournisseur_create/$', views.FournisseurCreateView.as_view(),
            name='fournisseur_create'),

]
