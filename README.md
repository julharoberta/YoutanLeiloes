# Youtan LeilÃµes

Sistema web para gerenciamento de leilÃµes, desenvolvido com Django, PostgreSQL, Bootstrap, JavaScript, jQuery e Docker.

## Funcionalidades

- Cadastro e gerenciamento de clientes.
- Cadastro e gerenciamento de instituiÃ§Ãµes financeiras.
- Cadastro e gerenciamento de leilÃµes.
- Cadastro de imÃ³veis e veÃ­culos vinculados a leilÃµes.
- Registro e consulta do histÃ³rico de lances.
- ValidaÃ§Ã£o das regras para registro de lances.
- Painel administrativo para gerenciamento dos cadastros.
- Interface web com acesso Ã  consulta de histÃ³rico de lances.

## Tecnologias utilizadas

- **Backend:** Python e Django.
- **Banco de dados:** PostgreSQL.
- **Frontend:** HTML5, CSS3, Bootstrap 5 e jQuery.
- **Servidor web:** Nginx.
- **API:** endpoints REST desenvolvidos com Django REST Framework.
- **Containers:** Docker e Docker Compose.
- **Testes:** testes automatizados do Django.

## PrÃ©-requisitos

Para executar a aplicaÃ§Ã£o com Docker, Ã© necessÃ¡rio ter o Docker Desktop instalado e em funcionamento.

## Como executar com Docker

1. Clone o repositÃ³rio:

   ```bash
   git clone https://github.com/julharoberta/YoutanLeiloes.git
   ```

2. Acesse a pasta:

   ```bash
   cd YoutanLeiloes
   ```

3. Inicie os serviÃ§os:

   ```bash
   docker compose up --build -d
   ```

   O Docker Compose iniciarÃ¡ o frontend, o backend e o banco de dados PostgreSQL. As migraÃ§Ãµes sÃ£o executadas na inicializaÃ§Ã£o do backend.

4. Acesse a aplicaÃ§Ã£o:

   - **Interface web:** http://localhost:8080
   - **Painel administrativo:** http://localhost:8080/admin/

5. Para criar um usuÃ¡rio administrador, caso necessÃ¡rio:

   ```bash
   docker compose exec backend python manage.py createsuperuser
   ```

## API

O histÃ³rico de lances pode ser consultado pelo endpoint:

```text
GET /api/lances/historico/
```

A consulta pode receber o identificador de um imÃ³vel ou veÃ­culo, conforme os parÃ¢metros implementados no backend.

A API tambÃ©m possui um endpoint para registro de lances, protegido por autenticaÃ§Ã£o administrativa.

## Executar os testes

Para executar os testes automatizados no ambiente Python local:

```bash
python manage.py test
```

O projeto possui 42 testes automatizados, aprovados na última execução.

## Encerrar os serviços

Para parar os containers sem remover os dados persistidos do banco:

```bash
docker compose down
```

Para iniciar novamente:

```bash
docker compose up -d
```

## ObservaÃ§Ãµes

As credenciais e configuraÃ§Ãµes definidas diretamente no arquivo `docker-compose.yml` sÃ£o destinadas ao ambiente local de desenvolvimento. Antes de utilizar a aplicaÃ§Ã£o em produÃ§Ã£o, configure senhas seguras, variÃ¡veis de ambiente e as opÃ§Ãµes de seguranÃ§a do Django.

## RepositÃ³rio

https://github.com/julharoberta/YoutanLeiloes


