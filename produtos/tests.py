
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import APITestCase

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

        # O leilão é cadastrado com datas futuras válidas.
        cls.leilao = Leilao.objects.create(
            titulo="Leilao para Testes",
            descricao="Leilao criado automaticamente para testes.",
            data_inicio=agora + timedelta(days=1),
            data_fim=agora + timedelta(days=2),
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

    def registrar_lance_com_leilao_aberto(
        self, valor, imovel_id=None, veiculo_id=None
    ):
        # Congela o relógio num instante em que o leilão está aberto.
        inicio = self.leilao.data_inicio
        momento = inicio + timedelta(hours=1)

        with freeze_time(momento):
            return registrar_lance(
                cliente_id=self.cliente.id,
                valor=valor,
                imovel_id=imovel_id,
                veiculo_id=veiculo_id,
            )

    # Validação de imóveis

    def test_rejeita_valor_inicial_zero_em_imovel(self):
        self.imovel.valor_inicial = Decimal("0.00")
        with self.assertRaises(ValidationError):
            self.imovel.save()

    def test_rejeita_incremento_minimo_negativo_em_imovel(self):
        self.imovel.incremento_minimo = Decimal("-1.00")
        with self.assertRaises(ValidationError):
            self.imovel.save()

    def test_normaliza_estado_do_imovel_para_maiusculas(self):
        self.imovel.estado = "sp"
        self.imovel.save()
        self.imovel.refresh_from_db()
        self.assertEqual(self.imovel.estado, "SP")

    # Validação de placa e RENAVAM

    def test_rejeita_placa_com_tamanho_invalido(self):
        self.veiculo.placa = "ABC123"
        with self.assertRaises(ValidationError):
            self.veiculo.save()

    def test_normaliza_placa_para_letras_maiusculas(self):
        self.veiculo.placa = "abc1d23"
        self.veiculo.save()
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.placa, "ABC1D23")

    def test_rejeita_renavam_com_mais_de_11_digitos(self):
        self.veiculo.renavam = "123456789012"
        with self.assertRaises(ValidationError):
            self.veiculo.save()

    def test_normaliza_renavam_removendo_caracteres_nao_numericos(self):
        self.veiculo.renavam = "123.456.789-01"
        self.veiculo.save()
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.renavam, "12345678901")

    # Registro de lances

    def test_registra_lance_valido(self):
        lance = self.registrar_lance_com_leilao_aberto(
            "101000.00", imovel_id=self.imovel.id
        )
        self.assertEqual(lance.valor, Decimal("101000.00"))
        self.assertEqual(lance.cliente, self.cliente)
        self.assertEqual(lance.imovel, self.imovel)
        self.assertIsNone(lance.veiculo)

    def test_rejeita_lance_abaixo_do_valor_minimo(self):
        with self.assertRaises(ValidationError):
            self.registrar_lance_com_leilao_aberto(
                "100500.00", imovel_id=self.imovel.id
            )
        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_lance_com_incremento_invalido(self):
        with self.assertRaises(ValidationError):
            self.registrar_lance_com_leilao_aberto(
                "101500.00", imovel_id=self.imovel.id
            )
        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_cliente_nao_autorizado(self):
        self.cliente.autorizado_a_dar_lances = False
        self.cliente.save()
        with self.assertRaises(ValidationError):
            self.registrar_lance_com_leilao_aberto(
                "101000.00", imovel_id=self.imovel.id
            )
        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_cliente_inativo(self):
        self.cliente.ativo = False
        self.cliente.save()
        with self.assertRaises(ValidationError):
            self.registrar_lance_com_leilao_aberto(
                "101000.00", imovel_id=self.imovel.id
            )
        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_lance_em_leilao_encerrado(self):
        agora = timezone.now()
        Leilao.objects.filter(pk=self.leilao.pk).update(
            data_inicio=agora - timedelta(days=2),
            data_fim=agora - timedelta(days=1),
        )
        self.leilao.refresh_from_db()

        with self.assertRaises(ValidationError):
            registrar_lance(
                cliente_id=self.cliente.id,
                valor="101000.00",
                imovel_id=self.imovel.id,
            )
        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_lance_sem_produto(self):
        with freeze_time(self.leilao.data_inicio + timedelta(hours=1)):
            with self.assertRaises(ValidationError):
                registrar_lance(
                    cliente_id=self.cliente.id,
                    valor="101000.00",
                )
        self.assertEqual(Lance.objects.count(), 0)

    def test_rejeita_lance_com_valor_nao_crescente(self):
        with freeze_time(self.leilao.data_inicio + timedelta(hours=1)):
            self.registrar_lance_com_leilao_aberto(
                "101000.00", imovel_id=self.imovel.id
            )
            with self.assertRaises(ValidationError):
                registrar_lance(
                    cliente_id=self.cliente.id,
                    valor="101000.00",
                    imovel_id=self.imovel.id,
                )
        self.assertEqual(Lance.objects.count(), 1)

    def test_rejeita_segundo_lance_com_incremento_insuficiente(self):
        with freeze_time(self.leilao.data_inicio + timedelta(hours=1)):
            self.registrar_lance_com_leilao_aberto(
                "101000.00", imovel_id=self.imovel.id
            )
            with self.assertRaises(ValidationError):
                registrar_lance(
                    cliente_id=self.cliente.id,
                    valor="101500.00",
                    imovel_id=self.imovel.id,
                )
        self.assertEqual(Lance.objects.count(), 1)

    def test_respeita_incremento_em_relacao_ao_ultimo_lance(self):
        self.imovel.valor_inicial = Decimal("4500.00")
        self.imovel.incremento_minimo = Decimal("200.00")
        self.imovel.save()

        with freeze_time(self.leilao.data_inicio + timedelta(hours=1)):
            primeiro = registrar_lance(
                cliente_id=self.cliente.id,
                valor="4700.00",
                imovel_id=self.imovel.id,
            )
            segundo = registrar_lance(
                cliente_id=self.cliente.id,
                valor="4900.00",
                imovel_id=self.imovel.id,
            )
            terceiro = registrar_lance(
                cliente_id=self.cliente.id,
                valor="5100.00",
                imovel_id=self.imovel.id,
            )

            self.assertEqual(primeiro.valor, Decimal("4700.00"))
            self.assertEqual(segundo.valor, Decimal("4900.00"))
            self.assertEqual(terceiro.valor, Decimal("5100.00"))

            with self.assertRaises(ValidationError):
                registrar_lance(
                    cliente_id=self.cliente.id,
                    valor="4885.00",
                    imovel_id=self.imovel.id,
                )
            with self.assertRaises(ValidationError):
                registrar_lance(
                    cliente_id=self.cliente.id,
                    valor="4600.00",
                    imovel_id=self.imovel.id,
                )

        self.assertEqual(Lance.objects.count(), 3)

    # Transferência de imóveis

    def criar_outro_leilao(self, titulo, endereco):
        agora = timezone.now()
        return Leilao.objects.create(
            titulo=titulo,
            descricao="Leilao para teste de transferencia.",
            data_inicio=agora + timedelta(days=1),
            data_fim=agora + timedelta(days=2),
            endereco=endereco,
            cidade="Taubate",
            estado="SP",
            instituicao_financeira=self.instituicao,
        )

    def test_bloqueia_transferencia_de_imovel_com_lances(self):
        self.registrar_lance_com_leilao_aberto(
            "101000.00", imovel_id=self.imovel.id
        )
        outro = self.criar_outro_leilao("Outro Leilao", "Rua Nova, 100")
        self.imovel.leilao = outro
        with self.assertRaises(ValidationError):
            self.imovel.save()

    def test_permite_transferencia_de_imovel_sem_lances(self):
        outro = self.criar_outro_leilao(
            "Leilao para Transferencia", "Rua Nova, 200"
        )
        self.imovel.leilao = outro
        self.imovel.save()
        self.imovel.refresh_from_db()
        self.assertEqual(self.imovel.leilao_id, outro.id)

    # Transferência de veículos

    def test_bloqueia_transferencia_de_veiculo_com_lances(self):
        self.registrar_lance_com_leilao_aberto(
            "51000.00", veiculo_id=self.veiculo.id
        )
        outro = self.criar_outro_leilao(
            "Outro Leilao para Veiculo", "Rua Nova, 300"
        )
        self.veiculo.leilao = outro
        with self.assertRaises(ValidationError):
            self.veiculo.save()

    def test_permite_transferencia_de_veiculo_sem_lances(self):
        outro = self.criar_outro_leilao(
            "Leilao para Transferir Veiculo", "Rua Nova, 400"
        )
        self.veiculo.leilao = outro
        self.veiculo.save()
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.leilao_id, outro.id)

    # Validação dos dados do veículo

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


class ApiLancesTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Usuario = get_user_model()
        cls.admin = Usuario.objects.create_user(
            username="admin_api_teste",
            password="senha-teste-123",
            is_staff=True,
        )

        cls.instituicao = InstituicaoFinanceira.objects.create(
            nome="Instituicao API Teste",
            cnpj="11222333000181",
        )

        agora = timezone.now()
        cls.leilao = Leilao.objects.create(
            titulo="Leilao API",
            descricao="Leilao para testar a API.",
            data_inicio=agora + timedelta(days=1),
            data_fim=agora + timedelta(days=2),
            endereco="Rua de Teste, 100",
            cidade="Taubate",
            estado="SP",
            instituicao_financeira=cls.instituicao,
        )

        cls.cliente_teste = Cliente.objects.create(
            nome="Cliente API",
            tipo_pessoa="PF",
            documento="52998224725",
            autorizado_a_dar_lances=True,
            ativo=True,
        )

        cls.imovel_teste = Imovel.objects.create(
            leilao=cls.leilao,
            tipo="RESIDENCIAL",
            matricula="API-MAT-001",
            cartorio="Cartorio API",
            descricao="Imovel para testes da API.",
            endereco="Rua de Teste, 200",
            cidade="Taubate",
            estado="SP",
            valor_inicial=Decimal("100000.00"),
            incremento_minimo=Decimal("1000.00"),
        )

    def setUp(self):
        self.client.force_authenticate(user=self.admin)

    def test_api_registra_lance_valido(self):
        with freeze_time(self.leilao.data_inicio + timedelta(hours=1)):
            resposta = self.client.post(
                "/api/lances/",
                {
                    "cliente_id": self.cliente_teste.id,
                    "valor": "101000.00",
                    "imovel_id": self.imovel_teste.id,
                },
                format="json",
            )

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(Lance.objects.count(), 1)

    def test_api_rejeita_usuario_sem_permissao(self):
        Usuario = get_user_model()
        usuario = Usuario.objects.create_user(
            username="usuario_comum_api",
            password="senha-teste-123",
            is_staff=False,
        )
        self.client.force_authenticate(user=usuario)

        with freeze_time(self.leilao.data_inicio + timedelta(hours=1)):
            resposta = self.client.post(
                "/api/lances/",
                {
                    "cliente_id": self.cliente_teste.id,
                    "valor": "101000.00",
                    "imovel_id": self.imovel_teste.id,
                },
                format="json",
            )

        self.assertEqual(resposta.status_code, 403)
        self.assertEqual(Lance.objects.count(), 0)

    def test_api_rejeita_lance_com_dados_invalidos(self):
        with freeze_time(self.leilao.data_inicio + timedelta(hours=1)):
            resposta = self.client.post(
                "/api/lances/",
                {
                    "cliente_id": self.cliente_teste.id,
                    "valor": "valor-invalido",
                    "imovel_id": self.imovel_teste.id,
                },
                format="json",
            )

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(Lance.objects.count(), 0)

    def test_api_consulta_historico_de_lances(self):
        with freeze_time(self.leilao.data_inicio + timedelta(hours=1)):
            registrar_lance(
                cliente_id=self.cliente_teste.id,
                valor="101000.00",
                imovel_id=self.imovel_teste.id,
            )

        self.client.force_authenticate(user=None)
        resposta = self.client.get(
            "/api/lances/historico/",
            {"imovel_id": self.imovel_teste.id},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.data), 1)
        self.assertEqual(resposta.data[0]["valor"], "101000.00")
        self.assertEqual(resposta.data[0]["cliente"], "Cliente API")
        self.assertEqual(
            resposta.data[0]["documento"],
            "***.***.***-25",
        )
        self.assertNotIn("52998224725", str(resposta.data))
