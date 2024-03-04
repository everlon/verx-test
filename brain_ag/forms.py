from django import forms

from django.forms import TextInput, CheckboxSelectMultiple

from brain_ag.models import ProdutorRural


class ProdutorCreateForm(forms.ModelForm):
    class Meta:
        model = ProdutorRural

        fields = (
            'cpf_cnpj', 
            'nome_produtor', 
            'nome_fazenda', 
            'cidade', 
            'estado', 
            'area_total', 
            'area_agricultavel', 
            'area_vegetacao',
            'cultura',
        )
        widgets = {
            'cpf_cnpj': forms.TextInput(attrs={'required': 'required'}),
            'nome_produtor': forms.TextInput(attrs={'required': 'required'}),
            'nome_fazenda': forms.TextInput(attrs={'required': 'required'}),
            'cidade': forms.TextInput(attrs={'required': 'required'}),
            'estado': forms.Select(attrs={'required': 'required'}),
            'area_total': forms.TextInput(attrs={'required': 'required'}),
            'area_agricultavel': forms.TextInput(attrs={'required': 'required'}),
            'area_vegetacao': forms.TextInput(attrs={'required': 'required'}),
            'cultura': CheckboxSelectMultiple(),
        }