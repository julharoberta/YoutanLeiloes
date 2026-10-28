
from django.contrib import admin
from django.urls import include, path

from clientes.views import listar_clientes_autorizados

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("produtos.urls")),
    path(
        "api/clientes/autorizados/",
        listar_clientes_autorizados,
        name="listar_clientes_autorizados",
    ),
]
