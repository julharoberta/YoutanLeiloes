
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import Lance
from .serializers import LanceEntradaSerializer
from .services import registrar_lance


def mascarar_documento(documento):
    """Oculta parte do CPF ou CNPJ, preservando apenas os últimos dígitos."""
    digitos = "".join(caractere for caractere in documento if caractere.isdigit())

    if len(digitos) == 11:
        return f"***.***.***-{digitos[-2:]}"
    if len(digitos) == 14:
        return f"**.***.***/****-{digitos[-2:]}"
    return "Documento não disponível"


@api_view(["POST"])
@permission_classes([IsAdminUser])
def criar_lance(request):
    serializer = LanceEntradaSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    dados = serializer.validated_data

    try:
        lance = registrar_lance(
            cliente_id=dados["cliente_id"],
            valor=dados["valor"],
            imovel_id=dados.get("imovel_id"),
            veiculo_id=dados.get("veiculo_id"),
        )
    except ValidationError as erro:
        return Response(
            {"erro": erro.messages},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except ObjectDoesNotExist:
        return Response(
            {"erro": "Cliente ou produto não encontrado."},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        {
            "mensagem": "Lance registrado com sucesso.",
            "lance_id": lance.id,
            "cliente": lance.cliente.nome,
            "valor": str(lance.valor),
            "imovel_id": lance.imovel_id,
            "veiculo_id": lance.veiculo_id,
            "criado_em": lance.criado_em.isoformat(),
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def historico_lances(request):
    imovel_id = request.query_params.get("imovel_id")
    veiculo_id = request.query_params.get("veiculo_id")

    if (imovel_id is None) == (veiculo_id is None):
        return Response(
            {
                "erro": (
                    "Informe exatamente um produto: "
                    "imovel_id ou veiculo_id."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    filtros = (
        {"imovel_id": imovel_id}
        if imovel_id is not None
        else {"veiculo_id": veiculo_id}
    )

    lances = (
        Lance.objects.filter(**filtros)
        .select_related("cliente")
        .order_by("id")
    )

    resultado = [
        {
            "lance_id": lance.id,
            "cliente": lance.cliente.nome,
            "documento": mascarar_documento(lance.cliente.documento),
            "valor": str(lance.valor),
            "criado_em": lance.criado_em.isoformat(),
        }
        for lance in lances
    ]

    return Response(resultado, status=status.HTTP_200_OK)
