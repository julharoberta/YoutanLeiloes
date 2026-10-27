
from django.db import models
from django.core.exceptions import ValidationError
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
    valor_inicial = models.DecimalField(max_digits=14, decimal_places=2)
    incremento_minimo = models.DecimalField(max_digits=14, decimal_places=2)
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

    def clean(self):
        super().clean()

        if self.valor_inicial is not None and self.valor_inicial <= 0:
            raise ValidationError({
                "valor_inicial": "O valor inicial deve ser maior que zero."
            })

        if self.incremento_minimo is not None and self.incremento_minimo <= 0:
            raise ValidationError({
                "incremento_minimo": "O incremento mínimo deve ser maior que zero."
            })

        if self.estado and len(self.estado.strip()) != 2:
            raise ValidationError({
                "estado": "Informe a sigla do estado com duas letras."
            })

        if self.estado:
            self.estado = self.estado.strip().upper()

    def save(self, *args, **kwargs):
        if self.pk:
            leilao_anterior = (
                Imovel.objects.filter(pk=self.pk)
                .values_list("leilao_id", flat=True)
                .first()
            )

            if (
                leilao_anterior is not None
                and leilao_anterior != self.leilao_id
                and Lance.objects.filter(imovel_id=self.pk).exists()
            ):
                raise ValidationError(
                    "Não é possível transferir um imóvel "
                    "que já recebeu lances para outro leilão."
                )

        self.full_clean()
        super().save(*args, **kwargs)

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
    valor_inicial = models.DecimalField(max_digits=14, decimal_places=2)
    incremento_minimo = models.DecimalField(max_digits=14, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"

    def clean(self):
        super().clean()

        if self.valor_inicial is not None and self.valor_inicial <= 0:
            raise ValidationError({
                "valor_inicial": "O valor inicial deve ser maior que zero."
            })

        if self.incremento_minimo is not None and self.incremento_minimo <= 0:
            raise ValidationError({
                "incremento_minimo": "O incremento mínimo deve ser maior que zero."
            })

        if (
            self.ano_fabricacao
            and self.ano_modelo
            and self.ano_modelo < self.ano_fabricacao
        ):
            raise ValidationError({
                "ano_modelo": (
                    "O ano do modelo não pode ser anterior "
                    "ao ano de fabricação."
                )
            })

        if self.chassi:
            self.chassi = self.chassi.strip().upper()

            if len(self.chassi) != 17:
                raise ValidationError({
                    "chassi": "O chassi deve conter exatamente 17 caracteres."
                })

            if any(letra in self.chassi for letra in "IOQ"):
                raise ValidationError({
                    "chassi": "O chassi não pode conter as letras I, O ou Q."
                })

        if self.placa:
            self.placa = self.placa.strip().upper().replace("-", "")

            if len(self.placa) != 7 or not self.placa.isalnum():
                raise ValidationError({
                    "placa": "Informe uma placa válida com 7 caracteres."
                })

        if self.renavam:
            self.renavam = "".join(
                caractere for caractere in self.renavam
                if caractere.isdigit()
            )

            if not 1 <= len(self.renavam) <= 11:
                raise ValidationError({
                    "renavam": "O RENAVAM deve conter de 1 a 11 dígitos."
                })

    def save(self, *args, **kwargs):
        if self.pk:
            leilao_anterior = (
                Veiculo.objects.filter(pk=self.pk)
                .values_list("leilao_id", flat=True)
                .first()
            )

            if (
                leilao_anterior is not None
                and leilao_anterior != self.leilao_id
                and Lance.objects.filter(veiculo_id=self.pk).exists()
            ):
                raise ValidationError(
                    "Não é possível transferir um veículo "
                    "que já recebeu lances para outro leilão."
                )

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.chassi}"


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
    valor = models.DecimalField(max_digits=14, decimal_places=2)
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
