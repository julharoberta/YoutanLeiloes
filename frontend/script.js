
$(document).ready(function () {
    $("#formHistorico").on("submit", function (event) {
        event.preventDefault();

        const tipoProduto = $("#tipoProduto").val();
        const produtoId = $("#produtoId").val();
        const $mensagem = $("#mensagem");
        const $resultado = $("#resultadoLances");

        $mensagem
            .removeClass("text-danger text-success")
            .text("Consultando histórico de lances...");

        $resultado.empty();

        const parametros = {};
        parametros[tipoProduto] = produtoId;

        $.ajax({
            url: "/api/lances/historico/",
            method: "GET",
            data: parametros,
            dataType: "json",

            success: function (resposta) {
                const lances = Array.isArray(resposta)
                    ? resposta
                    : (resposta.results || resposta.lances || []);

                if (lances.length === 0) {
                    $mensagem
                        .removeClass("text-danger")
                        .text("Nenhum lance encontrado para este produto.");

                    $resultado.append(
                        $("<tr>").append(
                            $("<td>")
                                .attr("colspan", 5)
                                .addClass("text-secondary")
                                .text("Não existem lances registrados.")
                        )
                    );
                    return;
                }

                $mensagem
                    .removeClass("text-danger")
                    .addClass("text-success")
                    .text("Histórico carregado com sucesso.");

                lances.forEach(function (lance) {
                    const valor = Number(
                        lance.valor_lance ?? lance.valor ?? lance.valor_ofertado
                    );

                    const valorFormatado = Number.isFinite(valor)
                        ? valor.toLocaleString("pt-BR", {
                            style: "currency",
                            currency: "BRL"
                        })
                        : "-";

                    const data = lance.criado_em || lance.data || lance.data_lance;

                    const dataFormatada = data
                        ? new Date(data).toLocaleString("pt-BR")
                        : "-";

                    const linha = $("<tr>");

                    linha.append($("<td>").text(lance.lance_id ?? lance.id ?? "-"));
                    linha.append($("<td>").text(lance.cliente_nome ?? lance.cliente ?? "-"));
                    linha.append($("<td>").text(lance.documento ?? "-"));
                    linha.append($("<td>").text(valorFormatado));
                    linha.append($("<td>").text(dataFormatada));

                    $resultado.append(linha);
                });
            },

            error: function (xhr) {
                $mensagem
                    .removeClass("text-success")
                    .addClass("text-danger")
                    .text(
                        xhr.responseJSON?.erro ||
                        xhr.responseJSON?.detail ||
                        "Não foi possível consultar os lances. Verifique o ID e tente novamente."
                    );

                $resultado.append(
                    $("<tr>").append(
                        $("<td>")
                            .attr("colspan", 5)
                            .addClass("text-secondary")
                            .text("Não foi possível carregar os resultados.")
                    )
                );
            }
        });
    });
});
