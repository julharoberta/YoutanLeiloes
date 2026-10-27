
from decimal import Decimal
from rest_framework import serializers

from clientes.models import Cliente
from .models import Imovel, Veiculo


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
