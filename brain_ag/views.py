import io, base64
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_cpf_cnpj.fields import CPFField, CNPJField

import matplotlib.pyplot as plt #Back-end

from brain_ag.models import ProdutorRural, CulturaPlantada
from brain_ag.forms import ProdutorCreateForm


def calculo_area(area_total, area_agricola, area_vegetacao):
    # Verifica se a soma da área agrícola e da vegetação não ultrapassa a área total da fazenda.
    soma_areas = area_agricola + area_vegetacao
    return soma_areas <= area_total


def save_plot_as_image_64(fig):
    img = io.BytesIO()
    fig.savefig(img, format="png", bbox_inches='tight')
    img.seek(0)
    plt.close(fig)
    return base64.b64encode(img.getvalue())


class HomeView(ListView):
    model = ProdutorRural
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['graf_estados'] = self.model.contar_estados()
        context['graf_valores_produtores'] = self.model.valores_produtores()
        context['graf_contar_culturas'] = self.model.contar_culturas()
        context['graf_valores_usodesolo'] = self.model.valores_usodesolo()
        return context


class Home2View(TemplateView):
    template_name = 'home2.html'

    def plot_estados(self):
        estados = ProdutorRural.contar_estados()
        labels = list(estados.keys())
        sizes = list(estados.values())

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')

        return save_plot_as_image_64(fig)

    def plot_culturas(self):
        culturas = CulturaPlantada.objects.all()
        total_culturas = ProdutorRural.contar_culturas()
        
        labels = [ c.name for c in culturas ]
        sizes = [ tc['total_cultura'] for tc in total_culturas ]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')

        return save_plot_as_image_64(fig)

    def plot_area(self):
        graf_valores_usodesolo = ProdutorRural.valores_usodesolo()

        labels = ['Área agricultável', 'Área de vegetação']
        sizes = [graf_valores_usodesolo['total_area_agricultavel'], graf_valores_usodesolo['total_area_vegetacao']]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')

        return save_plot_as_image_64(fig)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['graf_valores_produtores'] = ProdutorRural.valores_produtores()
        context['grafico_estados'] = self.plot_estados()
        context['grafico_culturas'] = self.plot_culturas()
        context['grafico_areas'] = self.plot_area()
        return context


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
            
        # A soma de área agrícultável e vegetação, não deverá ser maior que a área total da fazenda
        area_agricultavel = form.cleaned_data.get('area_agricultavel')
        area_total = form.cleaned_data.get('area_total')
        area_vegetacao = form.cleaned_data.get('area_vegetacao')

        if not calculo_area(area_total, area_agricultavel, area_vegetacao):
            form.add_error('area_total', 'A soma de área agrícultável e vegetação, não deverá ser maior que a área total da fazenda.')
            return self.form_invalid(form)

        produtor.save()
        form.save_m2m()
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
        form.save_m2m()
        return redirect('produtores')


class ProdutorDel(LoginRequiredMixin, DeleteView):
    model = ProdutorRural
    success_url = reverse_lazy('produtores')
