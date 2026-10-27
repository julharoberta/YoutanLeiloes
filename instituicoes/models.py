
from django.db import models


class InstituicaoFinanceira(models.Model):
    nome = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Instituição financeira"
        verbose_name_plural = "Instituições financeiras"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} - {self.cnpj}"
