
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
        "incremento_minimo",
        "leilao",
        "criado_em",
    )
    search_fields = (
        "matricula",
        "cartorio",
        "cidade",
        "endereco",
        "leilao__titulo",
    )
    list_filter = ("tipo", "estado", "leilao")
    list_select_related = ("leilao",)
    readonly_fields = ("criado_em",)


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
        "incremento_minimo",
        "leilao",
        "criado_em",
    )
    search_fields = (
        "marca",
        "modelo",
        "chassi",
        "placa",
        "renavam",
        "leilao__titulo",
    )
    list_filter = ("tipo", "marca", "leilao")
    list_select_related = ("leilao",)
    readonly_fields = ("criado_em",)


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
        "veiculo__placa",
    )
    list_filter = ("criado_em",)
    list_select_related = ("cliente", "imovel", "veiculo")
    readonly_fields = ("criado_em",)
