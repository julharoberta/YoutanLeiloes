const listaLeiloes = document.getElementById("listaLeiloes");
const mensagemLeiloes = document.getElementById("mensagemLeiloes");

function escaparHTML(valor) {
    return String(valor ?? "").replace(/[&<>"']/g, caractere => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[caractere]);
}

function formatarMoeda(valor) {
    const numero = Number(valor);

    if (!Number.isFinite(numero)) {
        return "Valor não informado";
    }

    return numero.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}

function formatarData(data) {
    if (!data) return "Não informada";

    const dataFormatada = new Date(data);

    if (Number.isNaN(dataFormatada.getTime())) {
        return "Data inválida";
    }

    return dataFormatada.toLocaleString("pt-BR", {
        dateStyle: "short",
        timeStyle: "short"
    });
}

function criarCardProduto(produto, categoria) {
    const nome = categoria === "imovel"
        ? `Imóvel ${produto.tipo || ""}`
        : `${produto.marca || ""} ${produto.modelo || ""}`;

    const detalhes = categoria === "imovel"
        ? `${produto.endereco || ""} — ${produto.cidade || ""}/${produto.estado || ""}`
        : `Ano: ${produto.ano_modelo || produto.ano_fabricacao || "Não informado"}`;

    const chaveProduto = `${categoria}-${produto.id}`;

    return `
        <article class="produto-card">
            <p class="eyebrow">
                ${categoria === "imovel" ? "IMÓVEL" : "VEÍCULO"}
            </p>

            <h3>${escaparHTML(nome.trim())}</h3>

            <p>${escaparHTML(produto.descricao || "Sem descrição disponível.")}</p>

            <p>${escaparHTML(detalhes)}</p>

            <p class="produto-valor">
                Valor inicial:
                <strong>${formatarMoeda(produto.valor_inicial)}</strong>
            </p>

            <p>
                Incremento mínimo:
                ${formatarMoeda(produto.incremento_minimo)}
            </p>

            <p class="produto-identificador">
                Código do produto: ${escaparHTML(produto.id)}
            </p>

            <div class="acoes-produto">
                <button
                    type="button"
                    class="btn-lance btn-abrir-formulario"
                    data-categoria="${categoria}"
                    data-produto-id="${escaparHTML(produto.id)}"
                    aria-expanded="false"
                    aria-controls="form-lance-${chaveProduto}"
                >
                    Dar lance
                </button>

                <a
                    class="btn-lance btn-consultar-lances"
                    href="historico.html?${categoria === "imovel" ? "imovel_id" : "veiculo_id"}=${encodeURIComponent(produto.id)}"
                >
                    Consultar lances
                </a>
            </div>

            <div
                class="formulario-lance-container"
                id="form-lance-${chaveProduto}"
                hidden
            ></div>
        </article>
    `;
}

function criarCardLeilao(leilao) {
    const imoveis = (leilao.imoveis || [])
        .map(imovel => criarCardProduto(imovel, "imovel"))
        .join("");

    const veiculos = (leilao.veiculos || [])
        .map(veiculo => criarCardProduto(veiculo, "veiculo"))
        .join("");

    return `
        <article class="leilao-card">
            <div class="leilao-cabecalho">
                <p class="eyebrow">
                    LEILÃO #${escaparHTML(leilao.id)}
                </p>

                <h2>${escaparHTML(leilao.titulo)}</h2>

                <p>
                    ${escaparHTML(leilao.descricao || "Sem descrição disponível.")}
                </p>
            </div>

            <div class="leilao-informacoes">
                <p>
                    <strong>Instituição:</strong>
                    ${escaparHTML(leilao.instituicao_financeira_nome || "Não informada")}
                </p>

                <p>
                    <strong>Local:</strong>
                    ${escaparHTML(
                        [leilao.cidade, leilao.estado]
                            .filter(Boolean)
                            .join("/") || "Não informado"
                    )}
                </p>

                <p>
                    <strong>Endereço:</strong>
                    ${escaparHTML(leilao.endereco || "Não informado")}
                </p>

                <p>
                    <strong>Início:</strong>
                    ${escaparHTML(formatarData(leilao.data_inicio))}
                </p>

                <p>
                    <strong>Encerramento:</strong>
                    ${escaparHTML(formatarData(leilao.data_fim))}
                </p>
            </div>

            <h3 class="secao-produtos">Imóveis</h3>

            <div class="produtos-grid">
                ${imoveis || "<p>Nenhum imóvel cadastrado neste leilão.</p>"}
            </div>

            <h3 class="secao-produtos">Veículos</h3>

            <div class="produtos-grid">
                ${veiculos || "<p>Nenhum veículo cadastrado neste leilão.</p>"}
            </div>
        </article>
    `;
}

async function carregarLeiloes() {
    try {
        mensagemLeiloes.textContent = "Carregando leilões...";

        const resposta = await fetch("/api/leiloes/", {
            credentials: "same-origin"
        });

        if (!resposta.ok) {
            throw new Error(`Erro HTTP ${resposta.status}`);
        }

        const leiloes = await resposta.json();

        if (!Array.isArray(leiloes) || leiloes.length === 0) {
            listaLeiloes.innerHTML = "";
            mensagemLeiloes.textContent =
                "Nenhum leilão cadastrado no momento.";
            return;
        }

        listaLeiloes.innerHTML = leiloes
            .map(criarCardLeilao)
            .join("");

        mensagemLeiloes.textContent =
            `${leiloes.length} leilão(ões) encontrado(s).`;

    } catch (erro) {
        console.error("Erro ao carregar leilões:", erro);

        mensagemLeiloes.textContent =
            "Não foi possível carregar os leilões. Tente novamente mais tarde.";
    }
}

function criarFormularioLance(categoria, produtoId) {
    return `
        <div class="formulario-lance">
            <h4>Registrar lance</h4>

            <p>
                Produto:
                ${categoria === "imovel" ? "Imóvel" : "Veículo"}
                #${escaparHTML(produtoId)}
            </p>

            <div class="form-group">
                <label for="cliente-lance-${categoria}-${produtoId}">
                    Cliente autorizado
                </label>

                <select
                    id="cliente-lance-${categoria}-${produtoId}"
                    class="campo-cliente-lance"
                    required
                >
                    <option value="">Carregando clientes...</option>
                </select>
            </div>

            <div class="form-group">
                <label for="valor-lance-${categoria}-${produtoId}">
                    Valor do lance (R$)
                </label>

                <input
                    id="valor-lance-${categoria}-${produtoId}"
                    class="campo-valor-lance"
                    type="number"
                    min="0.01"
                    step="0.01"
                    inputmode="decimal"
                    placeholder="Ex.: 151000.00"
                    required
                >
            </div>

            <button
                type="button"
                class="btn-lance btn-enviar-lance"
            >
                Enviar lance
            </button>

            <p
                class="mensagem-formulario-lance"
                role="status"
                aria-live="polite"
            >
                Carregando clientes autorizados...
            </p>
        </div>
    `;
}

document.addEventListener("click", async function (evento) {
    const botaoAbrir = evento.target.closest(".btn-abrir-formulario");

    if (botaoAbrir) {
        const categoria = botaoAbrir.dataset.categoria;
        const produtoId = botaoAbrir.dataset.produtoId;

        const formulario = document.getElementById(
            `form-lance-${categoria}-${produtoId}`
        );

        if (!formulario) return;

        if (!formulario.hidden) {
            formulario.hidden = true;
            botaoAbrir.textContent = "Dar lance";
            botaoAbrir.setAttribute("aria-expanded", "false");
            return;
        }

        formulario.hidden = false;
        botaoAbrir.textContent = "Fechar formulário";
        botaoAbrir.setAttribute("aria-expanded", "true");

        formulario.innerHTML = criarFormularioLance(
            categoria,
            produtoId
        );

        await carregarClientesParaLance(formulario);
        return;
    }

    const botaoEnviar = evento.target.closest(".btn-enviar-lance");

    if (botaoEnviar) {
        const formulario = botaoEnviar.closest(
            ".formulario-lance-container"
        );

        if (!formulario) return;

        const categoria = formulario.id.startsWith("form-lance-imovel-")
            ? "imovel"
            : "veiculo";

        const produtoId = formulario.id.replace(
            `form-lance-${categoria}-`,
            ""
        );

        await enviarLance(formulario, categoria, produtoId);
    }
});

async function carregarClientesParaLance(formulario) {
    const seletor = formulario.querySelector(".campo-cliente-lance");
    const mensagem = formulario.querySelector(".mensagem-formulario-lance");

    try {
        const resposta = await fetch("/api/clientes/autorizados/", {
            credentials: "same-origin"
        });

        if (!resposta.ok) {
            throw new Error(
                resposta.status === 403
                    ? "Acesso negado. Entre no Django Admin como operador e atualize a página."
                    : `Não foi possível carregar os clientes (HTTP ${resposta.status}).`
            );
        }

        const clientes = await resposta.json();

        seletor.innerHTML =
            '<option value="">Selecione um cliente</option>';

        clientes.forEach(cliente => {
            const opcao = document.createElement("option");

            opcao.value = cliente.id;
            opcao.textContent = cliente.nome;

            seletor.appendChild(opcao);
        });

        if (clientes.length === 0) {
            mensagem.textContent =
                "Nenhum cliente ativo e autorizado a dar lances.";
            return;
        }

        mensagem.textContent =
            "Selecione o cliente e informe o valor do lance.";

    } catch (erro) {
        console.error("Erro ao carregar clientes:", erro);

        mensagem.textContent =
            erro.message || "Erro ao carregar clientes.";

        seletor.innerHTML =
            '<option value="">Não foi possível carregar</option>';
    }
}

function obterTokenCSRF() {
    const correspondencia = document.cookie.match(
        /(?:^|;\s*)csrftoken=([^;]*)/
    );

    return correspondencia
        ? decodeURIComponent(correspondencia[1])
        : "";
}

async function enviarLance(formulario, categoria, produtoId) {
    const seletor = formulario.querySelector(".campo-cliente-lance");
    const campoValor = formulario.querySelector(".campo-valor-lance");
    const mensagem = formulario.querySelector(".mensagem-formulario-lance");
    const botaoEnviar = formulario.querySelector(".btn-enviar-lance");

    if (!seletor || !campoValor || !mensagem || !botaoEnviar) {
        console.error("O formulário de lance está incompleto.");
        return;
    }

    const clienteId = seletor.value;
    const valorNumerico = Number(campoValor.value);

    if (!clienteId) {
        mensagem.textContent = "Selecione um cliente autorizado.";
        seletor.focus();
        return;
    }

    if (
        !campoValor.value ||
        !Number.isFinite(valorNumerico) ||
        valorNumerico <= 0
    ) {
        mensagem.textContent =
            "Informe um valor de lance válido maior que zero.";
        campoValor.focus();
        return;
    }

    const csrfToken = obterTokenCSRF();

    if (!csrfToken) {
        mensagem.textContent =
            "Token de segurança (CSRF) não encontrado. " +
            "Entre no Django Admin e recarregue a página.";
        return;
    }

    const dados = {
        cliente_id: Number(clienteId),
        valor: valorNumerico.toFixed(2)
    };

    dados[
        categoria === "imovel" ? "imovel_id" : "veiculo_id"
    ] = Number(produtoId);

    botaoEnviar.disabled = true;
    mensagem.textContent = "Registrando lance...";

    try {
        const resposta = await fetch("/api/lances/", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(dados)
        });

        const tipoConteudo = resposta.headers.get("content-type") || "";

        const resultado = tipoConteudo.includes("application/json")
            ? await resposta.json()
            : { detail: await resposta.text() };

        if (!resposta.ok) {
            const detalhes = resultado.detail
                || resultado.mensagem
                || JSON.stringify(resultado);

            throw new Error(
                `Não foi possível registrar o lance (HTTP ${resposta.status}): ${detalhes}`
            );
        }

        mensagem.textContent =
            resultado.mensagem || "Lance registrado com sucesso!";

        campoValor.value = "";

    } catch (erro) {
        console.error("Erro ao registrar lance:", erro);

        mensagem.textContent =
            erro.message || "Não foi possível registrar o lance.";

    } finally {
        botaoEnviar.disabled = false;
    }
}

carregarLeiloes();