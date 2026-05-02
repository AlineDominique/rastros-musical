# 🚀 Plano de Desenvolvimento Full-Stack: Rastros Musical

Este documento detalha todas as etapas para o MVP, unindo engenharia de dados, backend e visualização geográfica em um Monorepo.

## 🟢 Fase 1: Fundação e Infraestrutura (Docker & Docs)
- [X] **Documentação de Governança**: Revisar se todos os ADRs estão atualizados com a estrutura de Monorepo.
- [X] **Estruturar Diretórios**: Criar as pastas `/app` (Backend), `/web` (Frontend), `/data` e `/docs`.
- [X] **Configuração Docker**: Criar Dockerfile para Backend e docker-compose.yml para orquestração (Python 3.13).
- [X] **Setup de Qualidade**: Configurar Ruff, Pytest e Coverage com regras de omissão no pyproject.toml.
- [x] **CI/CD Inicial:** Configurar GitHub Actions para rodar o pipeline de make check.

## 🔵 Fase 2: Engenharia de Dados (Arquitetura Medallion)
- [ ] **Camada Bronze (Raw)**: Implementar script de ingestão do MusicBrainz para armazenamento de dados brutos.
- [ ] **Camada Silver (Trusted)**: Implementar lógica de normalização e mapeamento geográfico (LatAm vs Ásia) via Python.
- [ ] **Camada Gold (Refined)**: Criar tabelas analíticas agregadas por ano e região para alimentar a API.
- [ ] **Schemas Pydantic**: Definir contratos de dados para Artistas, Gêneros e Localização.
- [ ] **Setup de Dados:** Configurar extensões espaciais do DuckDB para suporte geográfico.

## 🟡 Fase 3: API de Serviços (FastAPI)
- [ ] **Endpoints de Séries Temporais**: Criar rotas para retornar a evolução de gêneros e migrações musicais.
- [ ] **Singleton de Banco**: Gerenciar conexões persistentes com o arquivo `.db` do DuckDB.
- [ ] **Documentação OpenAPI**: Validar schemas e exemplos no Swagger para consumo do Frontend.

## 🟠 Fase 4: Interface e Visualização (React + Deck.gl)
- [ ] **Setup do Framework (/web)**: Inicializar projeto React com suporte a i18n (PT/EN/ES) via Docker.
- [ ] **Integração Deck.gl**: Configurar `ArcLayer` e `IconLayer` para visualização geográfica dinâmica.
- [ ] **Componente Time-Slider**: Desenvolver controle para navegação pela linha do tempo histórica (1970 - 2026).
- [ ] **Dashboard de Métricas**: Criar gráficos para comparação de popularidade entre regiões.

## 🔴 Fase 5: DevOps e Deploy Automático (Gratuito)
- [ ] **Deploy Automático Backend**: Vincular pasta `/app` ao Render ou Koyeb.
- [ ] **Deploy Automático Frontend**: Vincular pasta `/web` à Vercel ou Netlify.
- [ ] **Auditoria de Dados Final**: Implementar check de consistência proativo antes do deploy.