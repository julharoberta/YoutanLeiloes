
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from clientes.models import Cliente
from produtos.models import Imovel, Veiculo, Lance


@transaction.atomic
def registrar_lance(cliente_id, valor, imovel_id=None, veiculo_id=None):
    if (imovel_id is None) == (veiculo_id is None):
        raise ValidationError(
            "Informe exatamente um produto: imóvel ou veículo."
        )

    cliente = Cliente.objects.get(pk=cliente_id)

    if not cliente.ativo:
        raise ValidationError("Este cliente está inativo.")

    if not cliente.autorizado_a_dar_lances:
        raise ValidationError("Este cliente não está autorizado a dar lances.")

    valor = Decimal(str(valor))

    if valor <= 0:
        raise ValidationError("O valor do lance deve ser maior que zero.")

    if imovel_id is not None:
        produto = Imovel.objects.select_for_update().get(pk=imovel_id)
    else:
        produto = Veiculo.objects.select_for_update().get(pk=veiculo_id)

    agora = timezone.now()
    leilao = produto.leilao

    if agora < leilao.data_inicio:
        raise ValidationError("Este leilão ainda não começou.")

    if agora > leilao.data_fim:
        raise ValidationError("Este leilão já foi encerrado.")

    if produto.incremento_minimo <= 0:
        raise ValidationError("O incremento mínimo deve ser maior que zero.")

    lances = Lance.objects.filter(
        **({"imovel": produto} if imovel_id is not None else {"veiculo": produto})
    ).order_by("-valor")

    ultimo_lance = lances.first()

    if ultimo_lance is None:
        valor_base = produto.valor_inicial
    else:
        valor_base = ultimo_lance.valor

    if valor <= valor_base:
        raise ValidationError(
            f"O lance deve ser maior que R$ {valor_base}."
        )

    diferenca = valor - produto.valor_inicial
    incremento = produto.incremento_minimo

    if diferenca < 0 or diferenca % incremento != 0:
        raise ValidationError(
            "O lance deve respeitar o incremento mínimo do produto."
        )

    return Lance.objects.create(
        cliente=cliente,
        valor=valor,
        imovel=produto if imovel_id is not None else None,
        veiculo=produto if veiculo_id is not None else None,
    )
