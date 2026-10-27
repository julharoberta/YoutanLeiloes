
from django.contrib import admin
from .models import InstituicaoFinanceira


@admin.register(InstituicaoFinanceira)
class InstituicaoFinanceiraAdmin(admin.ModelAdmin):
    list_display = ("nome", "cnpj", "telefone", "ativa")
    search_fields = ("nome", "cnpj")
    list_filter = ("ativa",)
