# Rastros Musical 🎵
**Rastros Musical** é uma plataforma de engenharia e visualização de dados projetada para rastrear a propagação e evolução de gêneros musicais entre a **América Latina** e a **Ásia**.

---

## 🌍 Internacionalização (i18n)
O projeto foi construído para ser multilíngue, suportando nativamente:
*   **Português** (BR)
*   **English** (US)
*   **Español** (ES)

## 🏗️ Stack Tecnológica
*   **Linguagem:** [Python 3.13](https://docs.python.org/3.13/) (Foco em Type Hinting & [Pydantic](https://docs.pydantic.dev/))
*   **Framework de API:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Motor de Dados:** [DuckDB](https://duckdb.org/) (Banco de dados OLAP in-process)[cite: 4, 6]
*   **Suporte Espacial:** [Extensão Spatial do DuckDB](https://duckdb.org/docs/extensions/spatial)
*   **Qualidade:** [Pytest](https://docs.pytest.org/) (Testes) & [Ruff](https://docs.astral.sh/ruff/) (Linter & Formatador)[cite: 1, 5, 6]
*   **Infraestrutura:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
*   **CI/CD:** [GitHub Actions](https://github.com/features/actions)
*   **Automação:** [GNU Make](https://www.gnu.org/software/make/)

## 📂 Estrutura do Projeto
```text
rastros_musical/
├── .github/workflows/  # Pipelines de CI/CD
├── app/                # Núcleo da Aplicação
│   ├── api/            # Endpoints FastAPI
│   ├── core/           # Lógica de Negócio & Projeções
│   ├── db/             # Camada de Dados (DuckDB)
│   └── schemas/        # Contratos de Dados (Pydantic)
├── data/               # Armazenamento Particionado
│   ├── raw/            # Dados Brutos Imutáveis
│   └── processed/      # Dados Limpos e Transformados
├── docs/               # Documentação Técnica
│   └── adr/            # Registros de Decisão de Arquitetura (ADRs)
├── docker-compose.yml  
└── Dockerfile
```


## 🚀 Como Começar

### Pré-requisitos
*   Docker & Docker Compose
*   Make (opcional, mas recomendado)

1. Clonar o repositório:

```bash git clone https://github.com/seu-usuario/rastros_musical.git```

2. Acessar a pasta

```bash cd rastros_musical```

### Fluxo de Desenvolvimento
Utilizamos um `Makefile` para padronizar operações comuns. Se não tiver o `make` instalado, pode executar os comandos entre colchetes diretamente no terminal.

1.  **Build do ambiente:**
    ```bash
    make build  # [docker-compose up --build]
    ```

2.  **Executar a aplicação:**
    ```bash
    make up     # [docker-compose up]
    ```

3.  **Executar Testes:**
    ```bash
    make test   # [docker-compose exec app pytest]
    ```

4.  **Lint & Formatação:**
    ```bash
    make lint    # [docker-compose exec app ruff check . --fix]
    make format  # [docker-compose exec app ruff format .]
    ```

## Documentação
Para informações detalhadas sobre decisões técnicas e justificativas arquiteturais, consulte os nossos Registros de Decisão de Arquitetura (ADRs) localizados em `docs/architeture/pt/`.
