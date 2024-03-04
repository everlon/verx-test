from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_cpf_cnpj.fields import CPFField, CNPJField

from brain_ag.models import ProdutorRural
from brain_ag.forms import ProdutorCreateForm


def calculo_area(area_total, area_agricola, area_vegetacao):
    # Verifica se a soma da área agrícola e da vegetação não ultrapassa a área total da fazenda.
    soma_areas = area_agricola + area_vegetacao
    return soma_areas <= area_total


class HomeView(TemplateView):
    template_name = 'home.html'


class ProdutorView(LoginRequiredMixin, ListView):
    model = ProdutorRural
    template_name = 'produtores_list.html'
    context_object_name = 'produtores_list'
    
    """
    def get_queryset(self):
        # Este filtro é para se somente irá ver os Produtores que o usuário cadastrou.
        return ProdutorRural.objects.filter(submitter=self.request.user)
    """


class ProdutorAdd(LoginRequiredMixin, CreateView):
    model = ProdutorRural
    template_name = 'produtor_form.html'
    form_class = ProdutorCreateForm
    success_url = reverse_lazy('produtores')

    def form_valid(self, form, *args, **kwargs):
        # Aqui irá cadastrar o ID do usuário LOGADO que cadastrou, caso queira separar os Produtores por usuário.
        produtor = form.save(commit=False)
        produtor.submitter = self.request.user

        # O sistema deverá validar CPF e CNPJ digitados incorretamente.
        cpf_cnpj = form.cleaned_data.get('cpf_cnpj')
        if len(cpf_cnpj) == 14:
            cpf_field = CPFField()
            try:
                produtor.cpf_cnpj = cpf_field.clean(cpf_cnpj, produtor)
            except:
                form.add_error('cpf_cnpj', 'CPF inválido.')
                return self.form_invalid(form)

        elif len(cpf_cnpj) == 18:
            cnpj_field = CNPJField()
            try:
                produtor.cpf_cnpj = cnpj_field.clean(cpf_cnpj, produtor)
            except:
                form.add_error('cpf_cnpj', 'CNPJ inválido.')
                return self.form_invalid(form)
                
        else:
            form.add_error('cpf_cnpj', 'CPF ou CNPJ inválido.')
            return self.form_invalid(form)

        produtor.save()
        return redirect('produtores')


class ProdutorEdit(LoginRequiredMixin, UpdateView):
    model = ProdutorRural
    template_name = 'produtor_form.html'
    form_class = ProdutorCreateForm
    success_url = reverse_lazy('produtores')

    def form_valid(self, form, *args, **kwargs):
        # Aqui irá cadastrar o ID do usuário LOGADO que cadastrou, caso queira separar os Produtores por usuário.
        produtor = form.save(commit=False)
        produtor.submitter = self.request.user

        # O sistema deverá validar CPF e CNPJ digitados incorretamente.
        cpf_cnpj = form.cleaned_data.get('cpf_cnpj')
        if len(cpf_cnpj) == 14:
            cpf_field = CPFField()
            try:
                produtor.cpf_cnpj = cpf_field.clean(cpf_cnpj, produtor)
            except:
                form.add_error('cpf_cnpj', 'CPF inválido.')
                return self.form_invalid(form)

        elif len(cpf_cnpj) == 18:
            cnpj_field = CNPJField()
            try:
                produtor.cpf_cnpj = cnpj_field.clean(cpf_cnpj, produtor)
            except:
                form.add_error('cpf_cnpj', 'CNPJ inválido.')
                return self.form_invalid(form)
                
        else:
            form.add_error('cpf_cnpj', 'CPF ou CNPJ inválido.')
            return self.form_invalid(form)

        
        # Verifica se a soma da área agrícola e da vegetação não ultrapassa a área total da fazenda.
        if not calculo_area(produtor.area_total, produtor.area_agricultavel, produtor.area_vegetacao):
            form.add_error('area_total', 'Verifique os valores de área. A soma da área agricultável e da vegetação não pode ultrapassa a área total informada.')
            form.add_error('area_agricultavel', 'Verifique os valores de área. A soma da área agricultável e da vegetação não pode ultrapassa a área total informada.')
            form.add_error('area_vegetacao', 'Verifique os valores de área. A soma da área agricultável e da vegetação não pode ultrapassa a área total informada.')
            return self.form_invalid(form)


        produtor.save()
        return redirect('produtores')


class ProdutorDel(LoginRequiredMixin, DeleteView):
    model = ProdutorRural
    success_url = reverse_lazy('produtores')
