
from django.contrib import admin
from .models import Imovel, Veiculo, Lance


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tipo",
        "matricula",
        "cidade",
        "estado",
        "valor_inicial",
        "leilao",
    )
    search_fields = ("matricula", "cartorio", "cidade", "endereco")
    list_filter = ("tipo", "estado", "leilao")


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tipo",
        "marca",
        "modelo",
        "ano_modelo",
        "chassi",
        "valor_inicial",
        "leilao",
    )
    search_fields = ("marca", "modelo", "chassi", "placa", "renavam")
    list_filter = ("tipo", "marca", "leilao")


@admin.register(Lance)
class LanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente",
        "imovel",
        "veiculo",
        "valor",
        "criado_em",
    )
    search_fields = (
        "cliente__nome",
        "cliente__documento",
        "imovel__matricula",
        "veiculo__chassi",
    )
    list_filter = ("criado_em",)
    readonly_fields = ("criado_em",)
