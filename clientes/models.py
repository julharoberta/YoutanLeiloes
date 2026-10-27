
from django.db import models
from django.core.exceptions import ValidationError

from core.validators import cpf_valido, cnpj_valido, somente_digitos


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

    def clean(self):
        super().clean()

        documento = somente_digitos(self.documento)

        if self.tipo_pessoa == "PF":
            if not cpf_valido(documento):
                raise ValidationError({
                    "documento": "Informe um CPF válido."
                })

        elif self.tipo_pessoa == "PJ":
            if not cnpj_valido(documento):
                raise ValidationError({
                    "documento": "Informe um CNPJ válido."
                })

        else:
            raise ValidationError({
                "tipo_pessoa": "Selecione PF ou PJ."
            })

    def save(self, *args, **kwargs):
        self.documento = somente_digitos(self.documento)
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]

    def __str__(self):
        return self.nome
