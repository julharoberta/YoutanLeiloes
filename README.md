# Youtan Leilões

Sistema web para gerenciamento de leilões, desenvolvido com Django, PostgreSQL, Bootstrap, JavaScript, jQuery e Docker.

## Funcionalidades

- Cadastro e gerenciamento de clientes.
- Cadastro e gerenciamento de instituições financeiras.
- Cadastro e gerenciamento de leilões.
- Cadastro de imóveis e veículos vinculados a leilões.
- Registro e consulta do histórico de lances.
- Validação das regras para registro de lances.
- Painel administrativo para gerenciamento dos cadastros.
- Interface web com acesso à consulta de histórico de lances.

## Tecnologias utilizadas

- **Backend:** Python e Django.
- **Banco de dados:** PostgreSQL.
- **Frontend:** HTML5, CSS3, Bootstrap 5 e jQuery.
- **Servidor web:** Nginx.
- **API:** endpoints REST desenvolvidos com Django REST Framework.
- **Containers:** Docker e Docker Compose.
- **Testes:** testes automatizados do Django.

## Pré-requisitos

Para executar a aplicação com Docker, é necessário ter o Docker Desktop instalado e em funcionamento.

## Como executar com Docker

1. Clone o repositório:

   ```bash
   git clone https://github.com/julharoberta/YoutanLeiloes.git
   ```

2. Acesse a pasta:

   ```bash
   cd YoutanLeiloes
   ```

3. Inicie os serviços:

   ```bash
   docker compose up --build -d
   ```

   O Docker Compose iniciará o frontend, o backend e o banco de dados PostgreSQL. As migrações são executadas na inicialização do backend.

4. Acesse a aplicação:

   - **Interface web:** http://localhost:8080
   - **Painel administrativo:** http://localhost:8080/admin/

5. Para criar um usuário administrador, caso necessário:

   ```bash
   docker compose exec backend python manage.py createsuperuser
   ```

## API

O histórico de lances pode ser consultado pelo endpoint:

```text
GET /api/lances/historico/
```

A consulta pode receber o identificador de um imóvel ou veículo, conforme os parâmetros implementados no backend.

A API também possui um endpoint para registro de lances, protegido por autenticação administrativa.

## Executar os testes

Para executar os testes automatizados no ambiente Python local:

```bash
python manage.py test
```

O projeto possui **38 testes automatizados**, aprovados na última execução.

## Encerrar os serviços

Para parar os containers sem remover os dados persistidos do banco:

```bash
docker compose down
```

Para iniciar novamente:

```bash
docker compose up -d
```

## Observações

As credenciais e configurações definidas diretamente no arquivo `docker-compose.yml` são destinadas ao ambiente local de desenvolvimento. Antes de utilizar a aplicação em produção, configure senhas seguras, variáveis de ambiente e as opções de segurança do Django.

## Repositório

https://github.com/julharoberta/YoutanLeiloes
