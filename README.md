# Sistema de Gerenciamento de Roupas

Este projeto foi desenvolvido para gerir o cadastro, a organização, o armazenamento, a venda e o controle de roupas de uma loja ou empresa do ramo de vestuário. A aplicação permite registrar roupas, categorias, marcas, clientes, funcionários, fornecedores, vendas e entradas de estoque.

## Funcionalidades

- CRUD de categorias
- CRUD de marcas
- CRUD de roupas
- CRUD de variações de roupa com tamanho, cor e estoque
- CRUD de clientes
- CRUD de funcionários
- CRUD de fornecedores
- CRUD de vendas
- CRUD de entradas de estoque
- suporte a SQLite para testes locais
- suporte a MySQL para produção
- uso de variáveis de ambiente para conexão com banco MySQL

## Tecnologias

- Streamlit
- SQLAlchemy
- SQLite
- MySQL
- uv

## Estrutura do projeto

- `src/`: código da aplicação
- `README.md`: documentação do sistema
- `.gitignore`: arquivos ignorados por Git
- `pyproject.toml`: configuração do ambiente

## Requisitos

- Python 3.12+
- uv

## Como executar

1. Instale as dependências:

```bash
uv sync
```

2. Execute a aplicação:

```bash
uv run streamlit run src/app.py
```

3. Opcionalmente, ative o ambiente localmente:

```bash
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Banco de dados

### SQLite

O sistema usa SQLite por padrão para desenvolvimento e testes locais.

### MySQL

Para produção, configure as variáveis de ambiente antes de executar:

```bash
set MYSQL_HOST=localhost
set MYSQL_PORT=3306
set MYSQL_DATABASE=roupas_loja
set MYSQL_USER=root
set MYSQL_PASSWORD=sua_senha
set APP_ENV=production
```

Em Linux/macOS:

```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_DATABASE=roupas_loja
export MYSQL_USER=root
export MYSQL_PASSWORD=sua_senha
export APP_ENV=production
```

Quando as variáveis de conexão estiverem disponíveis e o ambiente estiver em produção, a aplicação utilizará MySQL.

## Observações

- SQLite é o banco recomendado para ambiente local e testes.
- MySQL deve ser usado em produção.
- Os dados ficam persistidos de acordo com o banco configurado no ambiente executado.

## Domínio do sistema

O minimundo cobre o gerenciamento de:

- roupas e suas categorias
- marcas e fornecedores
- clientes e funcionários
- estoque e variações de tamanho e cor
- vendas e itens vendidos
- entradas de estoque e itens recebidos
