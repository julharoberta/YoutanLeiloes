
from django.db import models
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
        related_name="leiloes"
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Leilão"
        verbose_name_plural = "Leilões"
        ordering = ["data_inicio"]

    def __str__(self):
        return self.titulo
