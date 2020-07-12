from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django.db.models import Sum, ExpressionWrapper, FloatField, F
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView
import django_tables2 as tables
from django_tables2.config import RequestConfig
from Bill.models import Facture, Client, Fournisseur


# Create your views here.


def facture_detail_view(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    context = {}
    context['facture'] = facture
    return render(request, 'bill/facture_detail.html', context)


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
