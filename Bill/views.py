from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django.db.models import Sum, ExpressionWrapper, FloatField, F
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView, TemplateView
import django_tables2 as tables
from django_tables2 import MultiTableMixin
from django_tables2.config import RequestConfig
from Bill.models import Facture, Client, Fournisseur, LigneFacture, Produit


# Create your views here.


def facture_detail_view(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    context = {}
    context['facture'] = facture
    return render(request, 'bill/facture_detail.html', context)



##################################################     Clients     ##############################################


class ClientTable(tables.Table):
    action = '<a href="{% url "client_update" pk=record.id  %}" class="btn btn-warning">update</a>\
              <a href="{% url "client_delete" pk=record.id  %}" class="btn btn-danger">delete</a>\
             <a href="{% url "client_factures_list" pk=record.id %}" class="btn btn-danger">Liste Factures</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields = ('id', 'nom', 'prenom', 'adresse', 'chiffre_affaire')


class ClientsView(ListView):
    model = Client
    template_name = 'bill/clients_table.html'

    def get_context_data(self, **kwargs):
        context = super(ClientsView, self).get_context_data(**kwargs)

        queryset = Client.objects.values('id', 'nom', 'prenom', 'adresse').annotate(chiffre_affaire=Sum(
            ExpressionWrapper(F('facture__lignes__qte'), output_field=FloatField()) * F(
                'facture__lignes__produit__prix')))
        table = ClientTable(queryset)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context['table'] = table
        return context

class FactureListTable(tables.Table):
    action = '<a href="{% url "facture_table_detail" pk=record.id %}" class="btn btn-danger">Liste Lignes</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('id', 'date')


class FacturesView(ListView):
    model = Client
    template_name = 'bill/facture_table.html'

    def get_context_data(self, **kwargs):
        context = super(FacturesView, self).get_context_data(**kwargs)

        queryset = Facture.objects.values('id', 'date')
        table = FactureListTable(queryset)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context['table'] = table
        return context


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['nom', 'prenom', 'sexe', 'adresse', 'tel']
    template_name = 'bill/client_update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('clients_table')
        return form


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'bill/client_delete.html'

    def get_success_url(self):
        return reverse('clients_table')


class ClientCreateView(CreateView):
    model = Client
    template_name = 'bill/create_client.html'
    fields = ['id', 'nom', 'prenom', 'sexe', 'adresse', 'tel']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('clients_table')
        return form


class FactureTable(tables.Table):
    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('id', 'date', 'total')


class ClientFacturesListView(DetailView):
    template_name = 'bill/client_factures_list.html'
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientFacturesListView, self).get_context_data(**kwargs)
        queryset = Facture.objects.filter(client_id=self.kwargs.get('pk')).annotate(total=Sum(
            ExpressionWrapper(F('lignes__qte'), output_field=FloatField()) * F('lignes__produit__prix')))
        table = FactureTable(queryset)
        context['table'] = table
        return context




##################################################     Facture     ##############################################


class FactureCreateView(CreateView):
    model = Facture
    template_name = 'bill/create_facture.html'
    fields = ['client', 'date']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.fields['client'] = forms.ModelChoiceField(
            queryset=Client.objects.filter(id=self.kwargs.get('client_pk')), initial=0)
        form.fields['date'] = forms.DateField(
            widget=DatePickerInput(format='%m/%d/%Y')
        )
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client_factures_list', kwargs={'pk': self.kwargs.get('client_pk')})
        return form

##################################################     Fournisseur    ##############################################


class FournisseurTable(tables.Table):
    action = '<a href="{% url "fournisseur_update" pk=record.id %}" class="btn btn-warning">update</a>\
              <a href="{% url "fournisseur_delete" pk=record.id %}" class="btn btn-danger">delete</a>'

    edit = tables.TemplateColumn(action)

    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nom', 'prenom', 'adresse', 'tel')




class FournisseursView(ListView):
    model = Fournisseur
    template_name = 'bill/fournisseur_table.html'

    def get_context_data(self, **kwargs):
        context = super(FournisseursView, self).get_context_data(**kwargs)

        queryset = Fournisseur.objects.all()
        table = FournisseurTable(queryset)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context['table'] = table
        return context


class FournisseurUpdateView(UpdateView):
    model = Fournisseur
    fields = ['nom', 'prenom', 'adresse', 'tel']
    template_name = 'bill/fournisseur_update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur_table')
        return form


class FournisseurDeleteView(DeleteView):
    model = Fournisseur
    fields = ['nom', 'prenom', 'adresse', 'tel']
    template_name = 'bill/fournisseur_delete.html'

    def get_success_url(self):
        return reverse('fournisseur_table')

class FournisseurCreateView(CreateView):
    model = Fournisseur
    template_name = 'bill/create_fournisseur.html'
    fields = ['nom', 'prenom', 'adresse', 'tel']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur_table')
        return form


##################################################     Ligne Facture     ##############################################

class LigneFactureCreateView(CreateView):
    model = LigneFacture
    template_name = 'bill/create.html'
    fields = ['facture', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture'] = forms.ModelChoiceField(
            queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})
        return form


class LigneFactureUpdateView(UpdateView):
    model = LigneFacture
    template_name = 'bill/update.html'
    fields = ['facture', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture'] = forms.ModelChoiceField(
            queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})
        return form


class LigneFactureDeleteView(DeleteView):
    model = LigneFacture
    template_name = 'bill/delete.html'

    def get_success_url(self):
        return reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})


class LigneFactureTable(tables.Table):
    action = '<a href="{% url "lignefacture_update" pk=record.id facture_pk=record.facture.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "lignefacture_delete" pk=record.id facture_pk=record.facture.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = LigneFacture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__designation', 'produit__id', 'produit__prix', 'qte')


class FactureDetailView(DetailView):
    template_name = 'bill/facture_table_detail.html'
    model = Facture

    def get_context_data(self, **kwargs):
        context = super(FactureDetailView, self).get_context_data(**kwargs)

        table = LigneFactureTable(LigneFacture.objects.filter(facture=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 4}).configure(table)
        context['table'] = table
        return context

##################################################     Chiffre d'affaire     ##############################################


class CAClientTable(tables.Table):
    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields = ('chiffre_affaire','nom', 'prenom' )


class CAFournisseurTable(tables.Table):
    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap4.html"
        fields = ('chiffre_affaire', 'nom', 'prenom')


class DashboardTables(MultiTableMixin, TemplateView):
    template_name = 'bill/dashboard.html'
    table_pagination = {
        "per_page": 10
    }

    def get_tables(self):
        qs1 = Fournisseur.objects.values('nom', 'prenom', 'adresse').annotate(chiffre_affaire=Sum(
            ExpressionWrapper(F('products__facture__qte'), output_field=FloatField()) * F(
                'products__prix')))

        qs2= Client.objects.values('nom', 'prenom').annotate(chiffre_affaire=Sum(
            ExpressionWrapper(F('facture__lignes__qte'), output_field=FloatField()) * F(
                'facture__lignes__produit__prix'))).order_by('-chiffre_affaire')
        return [
            CAClientTable(qs2),
            CAFournisseurTable(qs1)

        ]




