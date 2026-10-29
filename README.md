# Youtan Leilões

Sistema web para gerenciamento de leilões de imóveis e veículos, desenvolvido com Python, Django, Django REST Framework, PostgreSQL, HTML5, CSS3, Bootstrap, JavaScript, jQuery, Nginx e Docker Compose.

## Funcionalidades

- Cadastro e gerenciamento de clientes.
- Cadastro e gerenciamento de instituições financeiras.
- Cadastro e gerenciamento de leilões.
- Cadastro de imóveis e veículos vinculados a leilões.
- Consulta pública dos leilões e produtos disponíveis.
- Registro de lances com validações de negócio.
- Validação do período do leilão e do incremento mínimo.
- Consulta do histórico de lances por produto.
- Exibição do cliente, documento parcialmente mascarado, valor e data do lance.
- Painel administrativo para gerenciamento dos cadastros.

## Tecnologias

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

Clone o repositório:

```bash
git clone https://github.com/julharoberta/YoutanLeiloes.git
cd YoutanLeiloes
```

Construa as imagens e inicie os serviços:

```bash
docker compose up --build -d
```

O Docker Compose inicia o frontend, o backend e o PostgreSQL. As migrações do Django são executadas automaticamente antes da inicialização do servidor backend.

Acesse:

- **Site:** http://localhost:8080/
- **Painel administrativo:** http://localhost:8080/admin/
- **Leilões:** http://localhost:8080/leiloes.html
- **Histórico de lances:** http://localhost:8080/historico.html

Para criar um usuário administrador, caso ainda não exista:

```bash
docker compose exec backend python manage.py createsuperuser
```

Para registrar lances pela interface atual, entre no Django Admin no mesmo navegador antes de acessar a página de leilões. O endpoint de registro exige autenticação e valida os dados no backend.

## API

### Consultar leilões

```http
GET /api/leiloes/
```

### Consultar clientes ativos e autorizados

Esse endpoint exige autenticação administrativa:

```http
GET /api/clientes/autorizados/
```

### Registrar um lance

O endpoint exige autenticação e recebe um cliente, um valor e exatamente um produto: imóvel ou veículo.

Exemplo de lance para imóvel:

```http
POST /api/lances/
Content-Type: application/json
```

```json
{
  "cliente_id": 1,
  "valor": "151000.00",
  "imovel_id": 1
}
```

O backend valida a autorização do cliente, o período do leilão e as regras de incremento mínimo. Um lance não deve ser considerado registrado até que a API confirme o sucesso.

### Consultar o histórico de lances

Para um imóvel:

```http
GET /api/lances/historico/?imovel_id=1
```

Para um veículo:

```http
GET /api/lances/historico/?veiculo_id=1
```

O histórico apresenta os dados do produto e os lances correspondentes, ordenados pelo identificador do lance.

## Executar verificações e testes

Verifique a configuração do Django:

```bash
docker compose exec backend python manage.py check
```

Execute os testes automatizados:

```bash
docker compose exec backend python manage.py test
```

Na última execução registrada, os **42 testes automatizados passaram**, sem falhas.

Verifique o estado dos containers:

```bash
docker compose ps
```

## Encerrar os serviços

Para parar os containers sem remover o volume persistente do banco de dados:

```bash
docker compose down
```

Para iniciar novamente:

```bash
docker compose up -d
```

## Observações de segurança

As configurações do ambiente local são destinadas ao desenvolvimento. Para produção, configure credenciais seguras por variáveis de ambiente, as opções de segurança do Django e um servidor WSGI ou ASGI apropriado.

## Repositório

https://github.com/julharoberta/YoutanLeiloes