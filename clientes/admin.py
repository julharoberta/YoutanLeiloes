
from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "tipo_pessoa",
        "documento",
        "email",
        "autorizado_a_dar_lances",
        "ativo",
    )
    search_fields = ("nome", "documento", "email")
    list_filter = ("tipo_pessoa", "autorizado_a_dar_lances", "ativo")
