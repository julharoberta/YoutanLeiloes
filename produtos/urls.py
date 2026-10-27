
from django.urls import path
from .views import criar_lance, historico_lances

app_name = "produtos"

urlpatterns = [
    path("lances/", criar_lance, name="criar_lance"),
    path("lances/historico/", historico_lances, name="historico_lances"),
]
