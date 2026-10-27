
from django.contrib import admin
from .models import Leilao


@admin.register(Leilao)
class LeilaoAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "data_inicio",
        "data_fim",
        "cidade",
        "estado",
        "instituicao_financeira",
    )
    search_fields = ("titulo", "cidade", "estado")
    list_filter = ("estado", "instituicao_financeira")
    date_hierarchy = "data_inicio"
