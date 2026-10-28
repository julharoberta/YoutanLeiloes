
from django.urls import path
from .views import criar_lance, historico_lances, listar_leiloes

app_name = "produtos"

urlpatterns = [
    path("leiloes/", listar_leiloes, name="listar_leiloes"),
    path("lances/", criar_lance, name="criar_lance"),
    path("lances/historico/", historico_lances, name="historico_lances"),
]
