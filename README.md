# Sistema de Cadastro de Currículos

Aplicação web desenvolvida em Flask para cadastro e consulta de currículos, com foco em boas práticas de segurança da informação.

## Funcionalidades

- Listagem de currículos cadastrados (nome e e-mail)
- Cadastro de novo currículo com validação de dados
- Visualização detalhada de um currículo

## Tecnologias

- **Python 3** + **Flask**
- **MySQL** (via Docker)
- **SQLAlchemy** (ORM)
- **Flask-WTF** (formulários com proteção CSRF)
- **WTForms** + **email-validator** (validação de campos)

## Pré-requisitos

- Python 3.10+
- Docker com imagem MySQL disponível

## Instalação

**1. Clone o repositório e acesse a pasta do projeto:**

```bash
git clone <url-do-repositorio>
cd Trabalho-de-Seguranca-da-Informacao-Curriculos
```

**2. Crie e ative o ambiente virtual:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

## Configuração do Banco de Dados

**1. Inicie o container MySQL:**

```bash
docker run -d \
  --name mysql-curriculos \
  -e MYSQL_ROOT_PASSWORD=katryn \
  -p 3306:3306 \
  mysql:latest
```

Se o container já existir, basta iniciá-lo:

```bash
docker start mysql-curriculos
```

**2. Inicialize o banco de dados (apenas na primeira vez):**

```bash
docker exec -i mysql-curriculos mysql -uroot -pkatryn < sql/dump.sql
```

Isso cria o banco `sistema_curriculos` e a tabela `curriculo`.

## Execução

```bash
source venv/bin/activate
python app.py
```

A aplicação estará disponível em `http://localhost:5000`.

## Estrutura do Projeto

```
.
├── app.py          # Rotas e inicialização da aplicação
├── config.py       # Configurações (banco de dados, chave secreta)
├── models.py       # Modelo de dados (SQLAlchemy)
├── forms.py        # Formulários com validação e sanitização
├── init_db.py      # Script auxiliar para criação do banco
├── requirements.txt
├── sql/
│   └── dump.sql    # Script SQL para criação do banco e tabela
├── static/         # Arquivos estáticos (CSS, JS)
└── templates/      # Templates HTML (Jinja2)
```

## Segurança

A aplicação implementa as seguintes proteções:

| Proteção | Implementação |
|---|---|
| SQL Injection | Consultas parametrizadas via SQLAlchemy ORM |
| XSS (Cross-Site Scripting) | Sanitização com `html.escape` + Content Security Policy (CSP) |
| CSRF | Proteção global via Flask-WTF (`CSRFProtect`) |
| Clickjacking | Header `X-Frame-Options: DENY` |
| Cache de páginas sensíveis | Headers `Cache-Control: no-store` (prevenção de CSHM) |
| Sniffing de conteúdo | Header `X-Content-Type-Options: nosniff` |
