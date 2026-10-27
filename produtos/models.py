
from django.db import models
from leiloes.models import Leilao


class Imovel(models.Model):
    TIPO_IMOVEL = [
        ("RESIDENCIAL", "Residencial"),
        ("COMERCIAL", "Comercial"),
        ("RURAL", "Rural"),
    ]

    leilao = models.ForeignKey(
        Leilao,
        on_delete=models.PROTECT,
        related_name="imoveis",
    )

    tipo = models.CharField(max_length=20, choices=TIPO_IMOVEL)
    matricula = models.CharField(max_length=50)
    cartorio = models.CharField(max_length=150)
    descricao = models.TextField()
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    valor_inicial = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )
    incremento_minimo = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imóvel"
        verbose_name_plural = "Imóveis"
        constraints = [
            models.UniqueConstraint(
                fields=["matricula", "cartorio"],
                name="imovel_matricula_cartorio_unicos",
            ),
        ]

    def __str__(self):
        return f"{self.tipo} - Matrícula {self.matricula}"

    
class Veiculo(models.Model):
    TIPO_VEICULO = [
        ("MOTOCICLETA", "Motocicleta"),
        ("PASSEIO", "Veículo de passeio"),
        ("VAN", "Van"),
    ]

    leilao = models.ForeignKey(
        Leilao,
        on_delete=models.PROTECT,
        related_name="veiculos",
    )

    tipo = models.CharField(max_length=20, choices=TIPO_VEICULO)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano_fabricacao = models.PositiveIntegerField()
    ano_modelo = models.PositiveIntegerField()
    chassi = models.CharField(max_length=50, unique=True)
    placa = models.CharField(max_length=10, blank=True, null=True, unique=True)
    renavam = models.CharField(max_length=20, blank=True, null=True, unique=True)
    descricao = models.TextField(blank=True)

    valor_inicial = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )
    incremento_minimo = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.chassi}"


from django.conf import settings


class Lance(models.Model):
    imovel = models.ForeignKey(
        Imovel,
        on_delete=models.PROTECT,
        related_name="lances",
        null=True,
        blank=True,
    )
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        related_name="lances",
        null=True,
        blank=True,
    )
    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="lances",
    )
    valor = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        verbose_name = "Lance"
        verbose_name_plural = "Lances"
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    (
                        models.Q(imovel__isnull=False)
                        & models.Q(veiculo__isnull=True)
                    )
                    |
                    (
                        models.Q(imovel__isnull=True)
                        & models.Q(veiculo__isnull=False)
                    )
                ),
                name="lance_exatamente_um_produto",
            ),
        ]

    def __str__(self):
        return f"Lance de R$ {self.valor} - {self.cliente}"
