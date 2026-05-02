# Rastros Musical 🎵
**Rastros Musical** é uma plataforma de engenharia e visualização de dados projetada para rastrear a propagação e evolução de gêneros musicais entre a **América Latina** e a **Ásia**.

[Versão em Inglês(EN)](../../../README.md)

---

## 🌍 Internacionalização (i18n)
O projeto foi construído para ser multilíngue, suportando nativamente:
*   **Português** (BR)
*   **English** (US)
*   **Español** (ES)

## 🏗️ Stack Tecnológica

### Backend & Engenharia de Dados
*   **Linguagem:** [Python 3.13](https://docs.python.org/3.13/) (Foco em Type Hinting & [Pydantic](https://docs.pydantic.dev/))
*   **Framework de API:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Motor de Dados:** [DuckDB](https://duckdb.org/) (Banco de dados OLAP in-process)
*   **Suporte Espacial:** [DuckDB Spatial Extension](https://duckdb.org/docs/extensions/spatial)
*   **Garantia de Qualidade:** [Pytest](https://docs.pytest.org/) (Testes) & [Ruff](https://docs.astral.sh/ruff/) (Linter & Formatador)

### Frontend & Visualização
*   **Framework:** [React](https://react.dev/) (Interface & Gestão de Estado)
*   **Visualização:** [Deck.gl](https://deck.gl/) (Visualização de dados em larga escala via WebGL/GPU)
*   **Internacionalização:** [i18next](https://www.i18next.com/) (Suporte para PT/EN/ES)

### Infraestrutura & Automação
*   **Conteinerização:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
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
│   └── tests/          # Testes agora integrados ao backend
├── web/                # Frontend (React + Deck.gl) - Fase 4
├── data/               # Armazenamento Particionado
│   ├── raw/            # Dados Brutos Imutáveis
│   └── processed/      # Dados Limpos e Transformados
├── docs/               # Documentação Técnica
│   └── architecture/   # Registros de Decisão de Arquitetura (ADRs)
│       ├── pt/         # ADRs em Português
│       └── en          # ADRs em Inglês
├── MAkefile 
└── pyproject.toml
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
Para informações detalhadas sobre decisões técnicas e justificativas arquiteturais, consulte os nossos Registros de Decisão de Arquitetura **(ADRs)** localizados em `docs/architeture/pt/`.

## Gestão do Projeto

O planejamento estratégico e o acompanhamento de tarefas deste projeto estão centralizados em nossa documentação de gestão. Seguimos uma abordagem por fases para garantir a precisão inegociável dos dados exigida para este ecossistema.

Você pode acompanhar o progresso em tempo real aqui:
**[Roadmap de Desenvolvimento](../../../docs/management/todo-pt.md)**

### Status Atual:
- **Fase 1 (Fundação):** Concluída ✅
- **Fase 2 (Engenharia de Dados):** Em andamento