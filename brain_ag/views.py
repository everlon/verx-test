from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from brain_ag.models import ProdutorRural
from brain_ag.forms import ProdutorCreateForm


class HomeView(TemplateView):
    template_name = 'home.html'


class ProdutorView(LoginRequiredMixin, ListView):
    model = ProdutorRural
    template_name = 'produtores_list.html'
    context_object_name = 'produtores_list'
    
    def get_queryset(self):
        # Este filtro é para se somente irá ver os Produtores que o usuário cadastrou.
        return ProdutorRural.objects.filter(submitter=self.request.user)


class ProdutorAdd(LoginRequiredMixin, CreateView):
    model = ProdutorRural
    template_name = 'produtor_form.html'
    form_class = ProdutorCreateForm
    success_url = reverse_lazy('produtores')

    def form_valid(self, form, *args, **kwargs):
        # Aqui irá cadastrar o ID do usuário LOGADO que cadastrou, caso queira separar os Produtores por usuário.
        produtor = form.save(commit=False)
        produtor.submitter = self.request.user
        produtor.save()
        return redirect('produtores')


class ProdutorEdit(LoginRequiredMixin, UpdateView): 
    model = ProdutorRural
    template_name = 'produtor_form.html'
    form_class = ProdutorCreateForm
    success_url = reverse_lazy('produtores')


class ProdutorDel(LoginRequiredMixin, DeleteView):
    model = ProdutorRural
    success_url = reverse_lazy('produtores')
