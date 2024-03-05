# coverage run manage.py test
# coverage html
# py -m http.server --bind 127.0.0.1 9000 (servidor html)

from django.test import TestCase, Client
from model_mommy import mommy

from django.urls import reverse_lazy
import matplotlib.pyplot as plt
from django.urls import reverse
from django.forms.models import model_to_dict
from PIL import Image
from io import BytesIO

from django.contrib.auth.models import User
from brain_ag.models import ProdutorRural, CulturaPlantada
from brain_ag.views import calculo_area, save_plot_as_image_64, HomeView, Home2View
from brain_ag.forms import ProdutorCreateForm


class calculo_areaTestCase(TestCase):
    def setUp(self):
        self.area_total = 1000
        self.area_agricola = 900
        self.area_vegetacao = 100

    def test_calculo_area(self):
        self.assertTrue(calculo_area(self.area_total, self.area_agricola, self.area_vegetacao))


class save_plot_as_image_64TestCase(TestCase):
    def setUp(self):
        self.area1 = [1, 2, 3, 4]
        self.area2 = [1, 4, 2, 3]

    def test_save_plot_as_image_64(self):
        fig, ax = plt.subplots()
        ax.plot(self.area1, self.area2)

        result = save_plot_as_image_64(fig)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, bytes)
        
        plt.close(fig)


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_HomeView(self):
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('graf_estados', response.context)
        self.assertIn('graf_valores_produtores', response.context)
        self.assertIn('graf_contar_culturas', response.context)
        self.assertIn('graf_valores_usodesolo', response.context)


# class Home2ViewTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_Home2View(self):
#         response2 = self.client.get(reverse_lazy('backend'))
#         self.assertEqual(response2.status_code, 200)

#         print(response2.context)

        # self.assertIn('grafico_valores_produtores', response2.context)
        # self.assertIn('grafico_estados', response2.context)
        # self.assertIn('grafico_culturas', response2.context)
        # self.assertIn('grafico_areas', response2.context)

    # def test_plot_estados(self):
    #     response = self.client.get(reverse('backend'))
    #     self.assertEqual(response.status_code, 200)

    #     self.assertIn('image/png', response['Content-Type'])

    #     image_data = BytesIO(response.content)
    #     image = Image.open(image_data)
    #     self.assertTrue(image.width > 0)
    #     self.assertTrue(image.height > 0)


class ProdutorEditTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        self.cultura1 = model_to_dict(mommy.make('CulturaPlantada', pk=1, name="Soja"))
        self.cultura2 = model_to_dict(mommy.make('CulturaPlantada', pk=2, name="Milho"))
        self.cultura3 = model_to_dict(mommy.make('CulturaPlantada', pk=3, name="Algodão"))
        self.cultura4 = model_to_dict(mommy.make('CulturaPlantada', pk=4, name="Café"))
        self.cultura5 = model_to_dict(mommy.make('CulturaPlantada', pk=5, name="Cana de Açucar"))

        self.cliente = Client()
        self.cliente.login(username='testuser', password='testpassword')

        self.dados2 = {
            'pk': 1,
            'submitter': self.user,
            'nome_produtor': 'Nome do Produtor',
            'nome_fazenda': 'Fazenda Floresta',
            'cpf_cnpj': '944.473.542-76', # CPF válido
            'cidade': 'Alfenas',
            'estado': 'MG',
            'area_total': 1400,
            'area_agricultavel': 1100,
            'area_vegetacao': 300,
            'cultura': [self.cultura5['id'], self.cultura3['id'], self.cultura1['id'],]
        }

        self.cultura1_2 = mommy.make('CulturaPlantada', name="Soja")
        self.cultura2_2 = mommy.make('CulturaPlantada', name="Milho")
        self.cultura3_2 = mommy.make('CulturaPlantada', name="Algodão")
        self.cultura4_2 = mommy.make('CulturaPlantada', name="Café")
        self.cultura5_2 = mommy.make('CulturaPlantada', name="Cana de Açucar")

        self.produtor = ProdutorRural.objects.create(
            submitter= self.user,
            nome_produtor= 'Nome do Produtor',
            nome_fazenda= 'Fazenda Floresta',
            cpf_cnpj= '944.473.542-76', # CPF válido
            cidade= 'Alfenas',
            estado= 'MG',
            area_total= 1400,
            area_agricultavel= 1100,
            area_vegetacao= 300
        )
        self.produtor.cultura.add(self.cultura1_2, self.cultura3_2, self.cultura4_2)

    def test_form_valid(self):
        url = reverse_lazy('produtor-edit', kwargs={'pk':self.produtor.pk})
        request = self.cliente.post(url, data=self.dados2)
        
        # Salvar o retorno HTML para verificação.
        # with open('arquivo_saida_edit.html', 'wb') as arquivo:
        #     arquivo.write(request.content)

        self.assertEquals(request.status_code, 302)

    def test_form_invalid_cpf(self):
        form_data = {
            'nome_produtor': 'Nome do Produtor Editado',
            'nome_fazenda': 'Fazenda Nova Floresta',
            'cpf_cnpj': '11111111111111', # CPF inválido
            'cidade': 'Alfenas',
            'estado': 'MG',
            'area_total': 1200,
            'area_agricultavel': 900,
            'area_vegetacao': 300,
            'cultura': [self.cultura5['id'], self.cultura3['id'], self.cultura1['id'],]
        }

        request = self.cliente.post(reverse_lazy('produtor-edit', kwargs={'pk':self.produtor.pk}), data=form_data)

        # Salvar o retorno HTML para verificação.
        # with open('arquivo_saida_edit_invalid.html', 'wb') as arquivo:
        #     arquivo.write(request.content)

        self.assertEquals(request.status_code, 200)

    def test_form_invalid_cnpj(self):
        form_data = {
            'nome_produtor': 'Nome do Produtor Editado',
            'nome_fazenda': 'Fazenda Nova Floresta',
            'cpf_cnpj': '111111111111111111', # CNPJ inválido
            'cidade': 'Alfenas',
            'estado': 'MG',
            'area_total': 1200,
            'area_agricultavel': 900,
            'area_vegetacao': 300,
            'cultura': [self.cultura5['id'], self.cultura3['id'], self.cultura1['id'],]
        }

        request = self.cliente.post(reverse_lazy('produtor-edit', kwargs={'pk':self.produtor.pk}), data=form_data)

        # Salvar o retorno HTML para verificação.
        # with open('arquivo_saida_edit_invalid.html', 'wb') as arquivo:
        #     arquivo.write(request.content)

        self.assertEquals(request.status_code, 200)

    def test_form_invalid_else(self):
        form_data = {
            'nome_produtor': 'Nome do Produtor Editado',
            'nome_fazenda': 'Fazenda Nova Floresta',
            'cpf_cnpj': '111', # CPF/CNPJ inválido
            'cidade': 'Alfenas',
            'estado': 'MG',
            'area_total': 1200,
            'area_agricultavel': 900,
            'area_vegetacao': 300,
            'cultura': [self.cultura5['id'], self.cultura3['id'], self.cultura1['id'],]
        }

        request = self.cliente.post(reverse_lazy('produtor-edit', kwargs={'pk':self.produtor.pk}), data=form_data)

        # Salvar o retorno HTML para verificação.
        # with open('arquivo_saida_edit_invalid.html', 'wb') as arquivo:
        #     arquivo.write(request.content)

        self.assertEquals(request.status_code, 200)


class ProdutorAddTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        self.cultura1 = model_to_dict(mommy.make('CulturaPlantada', pk=1, name="Soja"))
        self.cultura2 = model_to_dict(mommy.make('CulturaPlantada', pk=2, name="Milho"))
        self.cultura3 = model_to_dict(mommy.make('CulturaPlantada', pk=3, name="Algodão"))
        self.cultura4 = model_to_dict(mommy.make('CulturaPlantada', pk=4, name="Café"))
        self.cultura5 = model_to_dict(mommy.make('CulturaPlantada', pk=5, name="Cana de Açucar"))

        self.cliente = Client()
        self.cliente.login(username='testuser', password='testpassword')

        self.dados2 = {
            'submitter': self.user,
            'nome_produtor': 'Nome do Produtor',
            'nome_fazenda': 'Fazenda Floresta',
            'cpf_cnpj': '944.473.542-76', # CPF válido
            'cidade': 'Alfenas',
            'estado': 'SP',
            'area_total': 1400,
            'area_agricultavel': 1100,
            'area_vegetacao': 300,
            'cultura': [self.cultura5['id'], self.cultura3['id'], self.cultura1['id'],]
        }

    def test_form_valid(self):
        url = reverse_lazy('produtor-add')
        request = self.cliente.post(url, data=self.dados2)
        
        # Salvar o retorno HTML para verificação.
        # with open('arquivo_saida_add.html', 'wb') as arquivo:
        #     arquivo.write(request.content)

        self.assertEquals(request.status_code, 302)

    def test_form_invalid_cpf(self):
        form_data = {
            'nome_produtor': 'Nome do Produtor Editado',
            'nome_fazenda': 'Fazenda Nova Floresta',
            'cpf_cnpj': '11111111111111', # CPF inválido
            'cidade': 'Alfenas',
            'estado': 'MG',
            'area_total': 1200,
            'area_agricultavel': 900,
            'area_vegetacao': 300,
            'cultura': [self.cultura5['id'], self.cultura3['id'], self.cultura1['id'],]
        }

        request = self.cliente.post(reverse_lazy('produtor-add'), data=form_data)

        # Salvar o retorno HTML para verificação.
        # with open('arquivo_saida_add_invalid.html', 'wb') as arquivo:
        #     arquivo.write(request.content)

        self.assertEquals(request.status_code, 200)

    def test_form_invalid_cnpj(self):
        form_data = {
            'nome_produtor': 'Nome do Produtor Editado',
            'nome_fazenda': 'Fazenda Nova Floresta',
            'cpf_cnpj': '111111111111111111', # CNPJ inválido
            'cidade': 'Alfenas',
            'estado': 'MG',
            'area_total': 1200,
            'area_agricultavel': 900,
            'area_vegetacao': 300,
            'cultura': [self.cultura5['id'], self.cultura3['id'], self.cultura1['id'],]
        }

        request = self.cliente.post(reverse_lazy('produtor-add'), data=form_data)

        # Salvar o retorno HTML para verificação.
        # with open('arquivo_saida_add_invalid.html', 'wb') as arquivo:
        #     arquivo.write(request.content)

        self.assertEquals(request.status_code, 200)

    def test_form_invalid_else(self):
        form_data = {
            'nome_produtor': 'Nome do Produtor Editado',
            'nome_fazenda': 'Fazenda Nova Floresta',
            'cpf_cnpj': '111', # CPF/CNPJ inválido
            'cidade': 'Alfenas',
            'estado': 'MG',
            'area_total': 1200,
            'area_agricultavel': 900,
            'area_vegetacao': 300,
            'cultura': [self.cultura5['id'], self.cultura3['id'], self.cultura1['id'],]
        }

        request = self.cliente.post(reverse_lazy('produtor-add'), data=form_data)

        # Salvar o retorno HTML para verificação.
        # with open('arquivo_saida_add_invalid.html', 'wb') as arquivo:
        #     arquivo.write(request.content)

        self.assertEquals(request.status_code, 200)

