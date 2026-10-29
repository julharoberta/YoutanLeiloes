
from decimal import Decimal
from rest_framework import serializers

from clientes.models import Cliente
from .models import Imovel, Veiculo

from leiloes.models import Leilao


class LanceEntradaSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField()
    valor = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )
    imovel_id = serializers.IntegerField(required=False)
    veiculo_id = serializers.IntegerField(required=False)

    def validate(self, dados):
        tem_imovel = "imovel_id" in dados
        tem_veiculo = "veiculo_id" in dados

        if tem_imovel == tem_veiculo:
            raise serializers.ValidationError(
                "Informe exatamente um produto: imóvel ou veículo."
            )

        if not Cliente.objects.filter(id=dados["cliente_id"]).exists():
            raise serializers.ValidationError(
                {"cliente_id": "Cliente não encontrado."}
            )

        if tem_imovel and not Imovel.objects.filter(
            id=dados["imovel_id"]
        ).exists():
            raise serializers.ValidationError(
                {"imovel_id": "Imóvel não encontrado."}
            )

        if tem_veiculo and not Veiculo.objects.filter(
            id=dados["veiculo_id"]
        ).exists():
            raise serializers.ValidationError(
                {"veiculo_id": "Veículo não encontrado."}
            )

        return dados

from leiloes.models import Leilao


class ImovelConsultaSerializer(serializers.ModelSerializer):
    leilao_titulo = serializers.CharField(
        source="leilao.titulo",
        read_only=True,
    )

    class Meta:
        model = Imovel
        fields = [
            "id",
            "leilao",
            "leilao_titulo",
            "tipo",
            "descricao",
            "endereco",
            "cidade",
            "estado",
            "valor_inicial",
            "incremento_minimo",
        ]


class VeiculoConsultaSerializer(serializers.ModelSerializer):
    leilao_titulo = serializers.CharField(
        source="leilao.titulo",
        read_only=True,
    )

    class Meta:
        model = Veiculo
        fields = [
            "id",
            "leilao",
            "leilao_titulo",
            "tipo",
            "marca",
            "modelo",
            "ano_fabricacao",
            "ano_modelo",
            "descricao",
            "valor_inicial",
            "incremento_minimo",
        ]


class LeilaoConsultaSerializer(serializers.ModelSerializer):
    instituicao_financeira_nome = serializers.CharField(
        source="instituicao_financeira.nome",
        read_only=True,
    )
    instituicao_financeira_cnpj = serializers.CharField(
        source="instituicao_financeira.cnpj",
        read_only=True,
    )
    instituicao_financeira_telefone = serializers.CharField(
        source="instituicao_financeira.telefone",
        read_only=True,
    )
    instituicao_financeira_email = serializers.CharField(
        source="instituicao_financeira.email",
        read_only=True,
    )
    instituicao_financeira_endereco = serializers.CharField(
        source="instituicao_financeira.endereco",
        read_only=True,
    )

    imoveis = ImovelConsultaSerializer(many=True, read_only=True)
    veiculos = VeiculoConsultaSerializer(many=True, read_only=True)

    class Meta:
        model = Leilao
        fields = [
            "id",
            "titulo",
            "descricao",
            "data_inicio",
            "data_fim",
            "endereco",
            "cidade",
            "estado",
            "instituicao_financeira_nome",
            "instituicao_financeira_cnpj",
            "instituicao_financeira_telefone",
            "instituicao_financeira_email",
            "instituicao_financeira_endereco",
            "imoveis",
            "veiculos",
        ]