
from django.db import models
from django.core.exceptions import ValidationError
from instituicoes.models import InstituicaoFinanceira


class Leilao(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    instituicao_financeira = models.ForeignKey(
        InstituicaoFinanceira,
        on_delete=models.PROTECT,
        related_name="leiloes",
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Leilão"
        verbose_name_plural = "Leilões"
        ordering = ["data_inicio"]

    def clean(self):
        super().clean()

        if (
            self.data_inicio
            and self.data_fim
            and self.data_fim <= self.data_inicio
        ):
            raise ValidationError({
                "data_fim": "A data final deve ser posterior à data inicial."
            })

        if self.estado and len(self.estado.strip()) != 2:
            raise ValidationError({
                "estado": "Informe a sigla do estado com duas letras."
            })

        if self.estado:
            self.estado = self.estado.strip().upper()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
