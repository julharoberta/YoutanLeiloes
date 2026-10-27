
from django.db import models


class Cliente(models.Model):
    TIPO_PESSOA = [
        ("PF", "Pessoa física"),
        ("PJ", "Pessoa jurídica"),
    ]

    nome = models.CharField(max_length=150)
    tipo_pessoa = models.CharField(
        max_length=2,
        choices=TIPO_PESSOA,
    )
    documento = models.CharField(max_length=18, unique=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    autorizado_a_dar_lances = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]

    def __str__(self):
        return self.nome
