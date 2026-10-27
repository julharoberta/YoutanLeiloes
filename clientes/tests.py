
from django.test import SimpleTestCase

from core.validators import cpf_valido, cnpj_valido, somente_digitos


class ValidadorDocumentosTests(SimpleTestCase):

    def test_aceita_cpf_valido(self):
        self.assertTrue(cpf_valido("52998224725"))

    def test_rejeita_cpf_invalido(self):
        self.assertFalse(cpf_valido("11111111111"))

    def test_aceita_cpf_formatado(self):
        self.assertTrue(cpf_valido("529.982.247-25"))

    def test_aceita_cnpj_valido(self):
        self.assertTrue(cnpj_valido("11222333000181"))

    def test_rejeita_cnpj_invalido(self):
        self.assertFalse(cnpj_valido("11111111111111"))

    def test_aceita_cnpj_formatado(self):
        self.assertTrue(cnpj_valido("11.222.333/0001-81"))

    def test_remove_caracteres_nao_numericos(self):
        self.assertEqual(
            somente_digitos("529.982.247-25"),
            "52998224725",
        )
