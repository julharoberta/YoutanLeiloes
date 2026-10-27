
from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from clientes.models import Cliente
from instituicoes.models import InstituicaoFinanceira
from leiloes.models import Leilao
from produtos.models import Imovel, Veiculo, Lance
from produtos.services import registrar_lance


class RegistrarLanceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.instituicao = InstituicaoFinanceira.objects.create(
            nome="Instituicao de Teste",
            cnpj="11222333000181",
        )

        agora = timezone.now()

        cls.leilao = Leilao.objects.create(
            titulo="Leilao para Testes",
            descricao="Leilao criado automaticamente para testes.",
            data_inicio=agora - timedelta(days=1),
            data_fim=agora + timedelta(days=1),
            endereco="Rua de Teste, 100",
            cidade="Taubate",
            estado="SP",
            instituicao_financeira=cls.instituicao,
        )

        cls.cliente = Cliente.objects.create(
            nome="Cliente Autorizado",
            tipo_pessoa="PF",
            documento="52998224725",
            autorizado_a_dar_lances=True,
            ativo=True,
        )

        cls.imovel = Imovel.objects.create(
            leilao=cls.leilao,
            tipo="RESIDENCIAL",
            matricula="TESTE-MAT-001",
            cartorio="Cartorio de Teste",
            descricao="Imovel para testes automatizados.",
            endereco="Rua de Teste, 200",
            cidade="Taubate",
            estado="SP",
            valor_inicial=Decimal("100000.00"),
            incremento_minimo=Decimal("1000.00"),
        )

        cls.veiculo = Veiculo.objects.create(
            leilao=cls.leilao,
            tipo="PASSEIO",
            marca="Toyota",
            modelo="Corolla",
            ano_fabricacao=2022,
            ano_modelo=2023,
            chassi="9BWZZZ377VT004251",
            placa="ABC1D23",
            renavam="12345678901",
            descricao="Veiculo para testes automatizados.",
            valor_inicial=Decimal("50000.00"),
            incremento_minimo=Decimal("1000.00"),
        )

    # Testes de registro de lances

    def test_registra_lance_valido(self):
        lance = registrar_lance(
            cliente_id=self.cliente.id,
            valor="101000.00",
            imovel_id=self.imovel.id,
        )

        self.assertEqual(lance.valor, Decimal("101000.00"))
        self.assertEqual(lance.cliente, self.cliente)
        self.assertEqual(lance.imovel, self.imovel)
        self.assertIsNone(lance.veiculo)

    def test_rejeita_lance_abaixo_do_valor_minimo(self):
        with self.assertRaises(ValidationError):
            registrar_lance(
                cliente_id=self.cliente.id,
                valor="100500.00",
                imovel_id=self.imovel.id,
            )

        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_lance_com_incremento_invalido(self):
        with self.assertRaises(ValidationError):
            registrar_lance(
                cliente_id=self.cliente.id,
                valor="101500.00",
                imovel_id=self.imovel.id,
            )

        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_cliente_nao_autorizado(self):
        self.cliente.autorizado_a_dar_lances = False
        self.cliente.save()

        with self.assertRaises(ValidationError):
            registrar_lance(
                cliente_id=self.cliente.id,
                valor="101000.00",
                imovel_id=self.imovel.id,
            )

        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_cliente_inativo(self):
        self.cliente.ativo = False
        self.cliente.save()

        with self.assertRaises(ValidationError):
            registrar_lance(
                cliente_id=self.cliente.id,
                valor="101000.00",
                imovel_id=self.imovel.id,
            )

        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_lance_em_leilao_encerrado(self):
        self.leilao.data_fim = timezone.now() - timedelta(days=1)
        self.leilao.save()

        with self.assertRaises(ValidationError):
            registrar_lance(
                cliente_id=self.cliente.id,
                valor="101000.00",
                imovel_id=self.imovel.id,
            )

        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_lance_sem_produto(self):
        with self.assertRaises(ValidationError):
            registrar_lance(
                cliente_id=self.cliente.id,
                valor="101000.00",
            )

        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_lance_com_valor_nao_crescente(self):
        registrar_lance(
            cliente_id=self.cliente.id,
            valor="101000.00",
            imovel_id=self.imovel.id,
        )

        with self.assertRaises(ValidationError):
            registrar_lance(
                cliente_id=self.cliente.id,
                valor="101000.00",
                imovel_id=self.imovel.id,
            )

        self.assertEqual(Lance.objects.count(), 1)

    # Testes de transferência de imóveis

    def test_bloqueia_transferencia_de_imovel_com_lances(self):
        registrar_lance(
            cliente_id=self.cliente.id,
            valor="101000.00",
            imovel_id=self.imovel.id,
        )

        outro_leilao = Leilao.objects.create(
            titulo="Outro Leilao",
            descricao="Leilao para testar transferencia.",
            data_inicio=timezone.now() - timedelta(days=1),
            data_fim=timezone.now() + timedelta(days=1),
            endereco="Rua Nova, 100",
            cidade="Taubate",
            estado="SP",
            instituicao_financeira=self.instituicao,
        )

        self.imovel.leilao = outro_leilao

        with self.assertRaises(ValidationError):
            self.imovel.save()

    def test_permite_transferencia_de_imovel_sem_lances(self):
        outro_leilao = Leilao.objects.create(
            titulo="Leilao para Transferencia",
            descricao="Leilao para testar transferencia sem lances.",
            data_inicio=timezone.now() - timedelta(days=1),
            data_fim=timezone.now() + timedelta(days=1),
            endereco="Rua Nova, 200",
            cidade="Taubate",
            estado="SP",
            instituicao_financeira=self.instituicao,
        )

        self.imovel.leilao = outro_leilao
        self.imovel.save()

        self.imovel.refresh_from_db()
        self.assertEqual(self.imovel.leilao_id, outro_leilao.id)

    # Testes de transferência de veículos

    def test_bloqueia_transferencia_de_veiculo_com_lances(self):
        registrar_lance(
            cliente_id=self.cliente.id,
            valor="51000.00",
            veiculo_id=self.veiculo.id,
        )

        outro_leilao = Leilao.objects.create(
            titulo="Outro Leilao para Veiculo",
            descricao="Teste de transferencia de veiculo com lance.",
            data_inicio=timezone.now() - timedelta(days=1),
            data_fim=timezone.now() + timedelta(days=1),
            endereco="Rua Nova, 300",
            cidade="Taubate",
            estado="SP",
            instituicao_financeira=self.instituicao,
        )

        self.veiculo.leilao = outro_leilao

        with self.assertRaises(ValidationError):
            self.veiculo.save()

    def test_permite_transferencia_de_veiculo_sem_lances(self):
        outro_leilao = Leilao.objects.create(
            titulo="Leilao para Transferir Veiculo",
            descricao="Teste de transferencia de veiculo sem lance.",
            data_inicio=timezone.now() - timedelta(days=1),
            data_fim=timezone.now() + timedelta(days=1),
            endereco="Rua Nova, 400",
            cidade="Taubate",
            estado="SP",
            instituicao_financeira=self.instituicao,
        )

        self.veiculo.leilao = outro_leilao
        self.veiculo.save()

        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.leilao_id, outro_leilao.id)

    # Testes de validação dos dados do veículo

    def test_rejeita_chassi_com_tamanho_invalido(self):
        self.veiculo.chassi = "ABC123"

        with self.assertRaises(ValidationError):
            self.veiculo.save()

    def test_rejeita_chassi_com_letras_proibidas(self):
        self.veiculo.chassi = "IOQ12345678901234"

        with self.assertRaises(ValidationError):
            self.veiculo.save()

    def test_rejeita_ano_modelo_anterior_ao_fabricacao(self):
        self.veiculo.ano_fabricacao = 2024
        self.veiculo.ano_modelo = 2023

        with self.assertRaises(ValidationError):
            self.veiculo.save()

    def test_rejeita_valor_inicial_zero(self):
        self.veiculo.valor_inicial = Decimal("0.00")

        with self.assertRaises(ValidationError):
            self.veiculo.save()

    def test_rejeita_incremento_minimo_negativo(self):
        self.veiculo.incremento_minimo = Decimal("-1.00")

        with self.assertRaises(ValidationError):
            self.veiculo.save()
