
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from instituicoes.models import InstituicaoFinanceira
from leiloes.models import Leilao


class LeilaoValidacaoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.instituicao = InstituicaoFinanceira.objects.create(
            nome="Instituição de Teste",
            cnpj="11222333000181",
        )

    def criar_leilao(self):
        agora = timezone.now()

        return Leilao(
            titulo="Leilão de Teste",
            descricao="Leilão utilizado para testes automatizados.",
            data_inicio=agora + timedelta(days=1),
            data_fim=agora + timedelta(days=2),
            endereco="Rua de Teste, 100",
            cidade="Taubaté",
            estado="sp",
            instituicao_financeira=self.instituicao,
        )

    def test_rejeita_data_inicio_no_passado(self):
        leilao = self.criar_leilao()
        leilao.data_inicio = timezone.now() - timedelta(days=1)
        leilao.data_fim = timezone.now() + timedelta(days=6)

        with self.assertRaises(ValidationError):
            leilao.save()

    def test_rejeita_data_final_anterior_ao_inicio(self):
        leilao = self.criar_leilao()
        leilao.data_fim = leilao.data_inicio - timedelta(days=1)

        with self.assertRaises(ValidationError):
            leilao.save()

    def test_rejeita_data_final_igual_ao_inicio(self):
        leilao = self.criar_leilao()
        leilao.data_fim = leilao.data_inicio

        with self.assertRaises(ValidationError):
            leilao.save()

    def test_normaliza_estado_para_letras_maiusculas(self):
        leilao = self.criar_leilao()
        leilao.save()

        leilao.refresh_from_db()
        self.assertEqual(leilao.estado, "SP")

    def test_rejeita_estado_com_tamanho_invalido(self):
        leilao = self.criar_leilao()
        leilao.estado = "SPO"

        with self.assertRaises(ValidationError):
            leilao.save()
