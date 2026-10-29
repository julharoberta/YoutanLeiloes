# Youtan Leilões

Sistema web para gerenciamento de leilões de imóveis e veículos, desenvolvido com Python, Django, Django REST Framework, PostgreSQL, HTML5, CSS3, Bootstrap, JavaScript, jQuery, Nginx e Docker Compose.

## Funcionalidades

- Cadastro e gerenciamento de clientes.
- Cadastro e gerenciamento de instituições financeiras.
- Cadastro e gerenciamento de leilões.
- Cadastro e gerenciamento de imóveis residenciais, comerciais e rurais.
- Cadastro e gerenciamento de motocicletas, veículos de passeio e vans.
- Associação obrigatória de imóveis e veículos a um leilão previamente cadastrado.
- Consulta pública dos leilões e dos produtos disponíveis.
- Exibição dos dados da instituição financeira associada ao leilão.
- Registro de lances com validações de negócio no backend.
- Validação da autorização do cliente e do período do leilão.
- Validação do valor inicial e do incremento mínimo dos lances.
- Consulta do histórico de lances por imóvel ou veículo.
- Exibição do cliente, documento parcialmente mascarado, valor e data do lance.
- Proteção de registros relacionados para preservar a integridade dos dados.

Os cadastros administrativos são gerenciados pela interface padrão do Django Admin.

## Tecnologias utilizadas

- **Backend:** Python, Django e Django REST Framework.
- **Banco de dados:** PostgreSQL.
- **Frontend:** HTML5, CSS3, Bootstrap, JavaScript e jQuery.
- **Servidor web:** Nginx.
- **Containers:** Docker e Docker Compose.
- **Testes:** testes automatizados do Django.

## Pré-requisitos

- Git instalado.
- Docker Desktop instalado e em execução.
- Docker Compose disponível pelo comando `docker compose`.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/julharoberta/YoutanLeiloes.git
cd YoutanLeiloes
```

### 2. Construir as imagens e iniciar os serviços

```bash
docker compose up --build -d
```

O Docker Compose inicia os serviços do frontend, backend e PostgreSQL. As migrações do Django são executadas automaticamente durante a inicialização do backend.

Para verificar o estado dos serviços:

```bash
docker compose ps
```

### 3. Acessar o sistema

Com os serviços em execução, acesse:

- **Página inicial:** http://localhost:8080/
- **Leilões:** http://localhost:8080/leiloes.html
- **Histórico de lances:** http://localhost:8080/historico.html
- **Painel administrativo:** http://localhost:8080/admin/

Os endereços com `localhost` funcionam no computador em que a aplicação está sendo executada.

### 4. Criar um usuário administrador

Caso ainda não exista um usuário administrador, execute:

```bash
docker compose exec backend python manage.py createsuperuser
```

Siga as instruções exibidas no terminal para cadastrar o usuário.

Para utilizar o formulário de registro de lances pela interface atual, entre no Django Admin no mesmo navegador antes de acessar a página de leilões.

O registro de lances exige autenticação e valida as regras de negócio no backend.

## API REST

### Consultar leilões

**Método:** `GET`

**Endpoint:**

```text
/api/leiloes/
```

Retorna os leilões cadastrados, os produtos associados e os dados disponíveis da instituição financeira vinculada a cada leilão.

### Consultar clientes autorizados

**Método:** `GET`

**Endpoint:**

```text
/api/clientes/autorizados/
```

O endpoint exige autenticação administrativa e retorna os clientes ativos e autorizados a dar lances.

### Registrar um lance

**Método:** `POST`

**Endpoint:**

```text
/api/lances/
```

**Content-Type:** `application/json`

Exemplo de requisição para registrar um lance em um imóvel:

```json
{
  "cliente_id": 1,
  "valor": "151000.00",
  "imovel_id": 1
}
```

Para registrar um lance em um veículo, utilize `veiculo_id` no lugar de `imovel_id`.

O backend valida, entre outros aspectos:

- A existência e a autorização do cliente.
- A existência do produto e sua associação a um leilão.
- O período de realização do leilão.
- O valor inicial e o incremento mínimo.
- A consistência do valor em relação ao último lance.

Um lance só deve ser considerado registrado após a confirmação de sucesso da API.

### Consultar o histórico de lances

Para um imóvel, utilize:

```text
GET /api/lances/historico/?imovel_id=1
```

Para um veículo, utilize:

```text
GET /api/lances/historico/?veiculo_id=1
```

O histórico apresenta as informações do produto e os lances correspondentes, incluindo cliente, valor e data. A ordenação é realizada pelo identificador do lance.

## Verificações e testes

### Verificar a configuração do Django

```bash
docker compose exec backend python manage.py check
```

### Executar os testes automatizados

```bash
docker compose exec backend python manage.py test
```

Na última execução registrada, os **42 testes automatizados passaram sem falhas**.

### Verificar os containers

```bash
docker compose ps
```

## Encerrar e reiniciar os serviços

Para parar os serviços sem remover o volume persistente do banco de dados:

```bash
docker compose down
```

Para iniciar novamente os serviços:

```bash
docker compose up -d
```

## Observações de segurança

As configurações locais são destinadas ao desenvolvimento. Para uso em produção, configure credenciais seguras por variáveis de ambiente, revise as opções de segurança do Django e utilize um servidor WSGI ou ASGI apropriado.

Não utilize credenciais de desenvolvimento em ambientes de produção.

## Repositório

https://github.com/julharoberta/YoutanLeiloes