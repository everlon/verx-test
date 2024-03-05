from django.test import TestCase
from model_mommy import mommy

from brain_ag.models import ProdutorRural, CulturaPlantada
from django.contrib.auth.models import User


class CulturaPlantadaTestCase(TestCase):
    def setUp(self):
        self.cultura = mommy.make('CulturaPlantada')

    def test_str(self):
        self.assertEquals(str(self.cultura), self.cultura.name)


class ProdutorRuralTestCase(TestCase):
    def setUp(self):
        """
        Fiz desta forma para ter o controle do valor gerado para análise.
        """

        # self.culturas = mommy.make('CulturaPlantada', _quantity=5)

        self.cultura1 = mommy.make('CulturaPlantada', name="Soja")
        self.cultura2 = mommy.make('CulturaPlantada', name="Milho")
        self.cultura3 = mommy.make('CulturaPlantada', name="Algodão")
        self.cultura4 = mommy.make('CulturaPlantada', name="Café")
        self.cultura5 = mommy.make('CulturaPlantada', name="Cana de Açucar")
        
        self.produtor1 = mommy.make('ProdutorRural', estado='ES', area_total=2000, area_agricultavel=1900, area_vegetacao=100, cultura=[self.cultura2, self.cultura3, self.cultura4])
        self.produtor2 = mommy.make('ProdutorRural', estado='MG', area_total=1000, area_agricultavel=800, area_vegetacao=200, cultura=[self.cultura2, self.cultura3, self.cultura4])
        self.produtor3 = mommy.make('ProdutorRural', estado='MG', area_total=2000, area_agricultavel=1800, area_vegetacao=1200, cultura=[self.cultura2, self.cultura4])
        self.produtor4 = mommy.make('ProdutorRural', estado='SP', area_total=3000, area_agricultavel=2000, area_vegetacao=1000, cultura=[self.cultura4, self.cultura5])
        self.produtor5 = mommy.make('ProdutorRural', estado='RJ', area_total=2000, area_agricultavel=1800, area_vegetacao=1200, cultura=[self.cultura1])


    def test_valores_produtores(self):
        valores = ProdutorRural.valores_produtores()

        self.assertEqual(valores['total_area'], 10000)
        self.assertEqual(valores['total_fazendas'], 5)

    def test_contar_estados(self):
        estados = ProdutorRural.contar_estados()
        
        # ES, 2 MG, SP e RJ
        self.assertEqual(len(estados), 4)

    def test_valores_usodesolo(self):
        areas = ProdutorRural.valores_usodesolo()

        self.assertEqual(areas['total_area_agricultavel'], 8300)
        self.assertEqual(areas['total_area_vegetacao'], 3700)

    def test_contar_culturas(self):
        total_culturas = ProdutorRural.contar_culturas()

        # Quantidades: 1 soja, 3 milho, 2 algodão, 4 café, 1 cana
        self.assertEqual(total_culturas[0]['total_cultura'], 2)
        self.assertEqual(total_culturas[1]['total_cultura'], 4)
        self.assertEqual(total_culturas[2]['total_cultura'], 1)
        self.assertEqual(total_culturas[3]['total_cultura'], 3)
        self.assertEqual(total_culturas[4]['total_cultura'], 1)

    def test_str(self):
        self.assertEquals(str(self.produtor1), self.produtor1.nome_produtor + ' - ' + self.produtor1.nome_fazenda)

