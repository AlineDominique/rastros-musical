# ADR-010: Fontes de dados para propagação musical

**Status:** Aceito  
**Data:** 2026-05-07  

---

## Contexto

A Fase 2 do MVP utilizou exclusivamente o MusicBrainz como fonte de dados. Durante a ingestão, foram identificados problemas de qualidade:

- Tags colaborativas imprecisas (ex: Coleman Hawkins como sambista)
- Datas de nascimento de artistas, não de produção musical
- Outliers geográficos (ex: K-Pop na Lituânia)
- Impossibilidade de validar a real propagação de gêneros

O MusicBrainz é um banco de dados de artistas, não de propagação de gêneros musicais.

## Decisão

Substituir o MusicBrainz por três fontes complementares:

| Fonte | Pergunta respondida | Tipo de dado |
|-------|---------------------|--------------|
| **Wikipedia** | Onde e quando o gênero surgiu? | Curadoria manual |
| **Google Trends** | Quando o gênero começou a ser buscado em cada país? | Série temporal |
| **Spotify Charts** | Onde o gênero é ouvido atualmente? | Popularidade por país |

O MusicBrainzClient será removido. O restante do pipeline (Medallion, DuckDB, testes) permanece intacto.

## Alternativas consideradas

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **Manter MusicBrainz** | Já está implementado | Dados imprecisos, não responde à pergunta do projeto |
| **MusicBrainz + curadoria manual** | Aproveita código existente | A curadoria não resolve o problema de fundo (datas de nascimento vs. produção) |
| **Wikipedia + Google Trends + Spotify** | Precisão, múltiplas dimensões | Requer implementação de novos clientes |

## Consequências

**Positivas:**
- Origem dos gêneros validada por curadoria humana (Wikipedia)
- Propagação temporal mensurável (Google Trends)
- Popularidade atual geolocalizada (Spotify Charts)
- Dados respondem diretamente à pergunta do projeto

**Negativas:**
- Google Trends requer biblioteca externa (`pytrends`) com suporte não oficial
- Spotify requer token de API com renovação
- Tabela manual de origem exige manutenção
- MusicBrainzClient e seus testes serão removidos

## Estrutura mantida

- Medallion Architecture (Bronze/Silver/Gold)
- DuckDB + Spatial Extension
- FastAPI
- Testes, CI/CD, logging
- Makefile, Docker