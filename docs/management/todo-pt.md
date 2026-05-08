# 🚀 Plano de Desenvolvimento Full-Stack: Rastros Musical

Este documento detalha todas as etapas para o MVP, unindo engenharia de dados, backend e visualização geográfica em um Monorepo.

---

## 🟢 Fase 1: Fundação e Infraestrutura (Docker & Docs)

### ✅ Concluído
- [X] **Documentação de Governança**: Revisar se todos os ADRs estão atualizados com a estrutura de Monorepo.
- [X] **Estruturar Diretórios**: Criar as pastas `/app` (Backend), `/web` (Frontend), `/data` e `/docs`.
- [X] **Configuração Docker**: Criar Dockerfile para Backend e docker-compose.yml para orquestração (Python 3.13).
- [X] **Setup de Qualidade**: Configurar Ruff, Pytest e Coverage com regras de omissão no pyproject.toml.
- [X] **CI/CD Inicial:** Configurar GitHub Actions para rodar o pipeline de make check.

---

## 🔵 Fase 2: Engenharia de Dados (Arquitetura Medallion)

### ✅ Concluído
- [X] **Schemas Pydantic**: Definir contratos de dados para Artistas, Gêneros e Localização.
- [X] **Setup de Dados:** Configurar extensões espaciais do DuckDB para suporte geográfico.

### 🎯 MVP (Múltiplas Fontes de Dados)
- [X] **Wikipedia (Origem)**: Tabela manual com país e ano de surgimento de cada gênero.
- [X] **Google Trends (Propagação)**: Cliente para buscar primeira busca significativa por país.
- [ ] **Camada Silver (Normalização)**: Integrar e limpar dados das três fontes.
- [ ] **Camada Gold Essencial**: Criar `gold.genre_first_appearance` com dados consolidados.


### 📈 Incrementações Futuras
- [ ] **Automação da ingestão**: Atualização periódica via GitHub Actions.
- [ ] **Validação cruzada**: Confrontar dados das três fontes para garantir consistência.
- [ ] **Spotify Charts (Popularidade)**: Cliente para obter popularidade atual por país.
- [ ] **Camada Silver (Normalização)**: Validação de `country_code` contra ISO 3166-1, normalização de nomes (strip, title case) e deduplicação de artistas com mesmo nome e país.
- [ ] **Camada Gold Avançada**: Tabelas analíticas de crescimento (`gold.genre_growth`), popularidade comparada e agregações temporais.

---

## 🟡 Fase 3: API de Serviços (FastAPI)

### 🎯 MVP (Dois Endpoints Essenciais)
- [ ] **Singleton de Banco**: Gerenciar conexões persistentes com o arquivo `.db` do DuckDB.
- [ ] **Endpoint de Gêneros**: `GET /api/genres` retornando a lista de gêneros únicos disponíveis.
- [ ] **Endpoint de Propagação**: `GET /api/propagation?genre=...&year=...` retornando os países onde o gênero apareceu até o ano informado (lat, lon, ano).
- [ ] **Documentação OpenAPI**: Escrever exemplos claros no Swagger para facilitar o consumo pelo frontend.

### 📈 Incrementações Futuras
- [ ] **Endpoints de Séries Temporais**: Rotas para evolução detalhada (lançamentos por ano/país) e métricas de migração.
- [ ] **Auditoria de Dados**: Health check que valida consistência das tabelas antes do deploy.

---

## 🟠 Fase 4: Interface e Visualização (React + Deck.gl)

### 🎯 MVP (Mapa Vivo com Controles Mínimos)
- [ ] **Setup do Framework (/web)**: Inicializar projeto React (Vite) sem i18n inicial.
- [ ] **Mapa com ScatterplotLayer**: Exibir pontos coloridos representando a primeira aparição do gênero nos países.
- [ ] **Dropdown de Gênero**: Selecionar um gênero da lista obtida da API.
- [ ] **Componente Time-Slider**: Slider (1970–2026) que dispara novas chamadas à API ao ser alterado.
- [ ] **Tooltip simples**: Mostrar país e ano ao passar o mouse sobre um ponto.

### 📈 Incrementações Futuras
- [ ] **Setup i18n**: Adicionar suporte a PT/EN/ES nos componentes da interface.
- [ ] **Integração ArcLayer / IconLayer**: Mostrar fluxos de origem/destino quando houver dado de país de origem.
- [ ] **Dashboard de Métricas**: Gráficos comparativos (ex.: popularidade entre regiões) abaixo do mapa.
- [ ] **Suporte a Múltiplos Gêneros**: Permitir selecionar mais de um gênero para comparação visual.

---

## 🔴 Fase 5: DevOps e Deploy Automático (Gratuito)

### 🎯 MVP (Deploy Manual com Link Público)
- [ ] **Deploy Backend**: Subir container da pasta `/app` no Fly.io.
- [ ] **Deploy Frontend**: Fazer build e deploy da pasta `/web` na Vercel.
- [ ] **Variáveis de Ambiente**: Configurar URL da API no frontend para apontar para o Fly.io.

### 📈 Incrementações Futuras
- [ ] **Deploy Automático Backend**: CI/CD completo vinculando o repositório ao Fly.io via GitHub Actions.
- [ ] **Deploy Automático Frontend**: CI/CD completo vinculando o repositório à Vercel via GitHub Actions.
- [ ] **Auditoria de Dados Final**: Check de consistência proativo executado no pipeline antes de cada deploy.
