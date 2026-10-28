
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Cliente


@api_view(["GET"])
@permission_classes([IsAdminUser])
def listar_clientes_autorizados(request):
    clientes = Cliente.objects.filter(
        ativo=True,
        autorizado_a_dar_lances=True,
    ).order_by("nome")

    resultado = [
        {
            "id": cliente.id,
            "nome": cliente.nome,
        }
        for cliente in clientes
    ]

    return Response(resultado, status=status.HTTP_200_OK)
