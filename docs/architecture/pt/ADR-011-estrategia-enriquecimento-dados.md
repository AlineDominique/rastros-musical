# ADR-011: Estratégia de Enriquecimento da Base de Dados de Propagação

**Status:** Aceito
**Data:** 2026-05-12

---

## Contexto

A Fase 2 do MVP foi concluída com 20 gêneros validados manualmente (Wikipedia) e dados de propagação via Google Trends. No entanto, o Google Trends só possui dados a partir de 2004, resultando em apenas 7 registros de propagação e um salto temporal de mais de 100 anos entre a origem de gêneros como o Tango (1880) e sua primeira busca registrada na Coreia do Sul (2004).

Para responder à pergunta central do projeto — "Como um gênero musical se espalha pelo mundo através do tempo?" — é necessário preencher essa lacuna com dados de propagação anteriores a 2004.

Após análise de múltiplas fontes (Musicmap, Google Music Timeline, Every Noise at Once, Radiooooo.com, Million Song Dataset), identificou-se que o **Million Song Dataset (MSD)** é a única base pública que oferece ano, país e coordenadas para um grande volume de músicas (1922–2011).

## Decisão

Adotar três fontes complementares para enriquecimento progressivo da base:

| Fonte | Função | Tipo de dado |
|-------|--------|--------------|
| **Musicmap** | Curadoria: refinar ano e local de origem dos 20 gêneros | Genealogia visual (consulta manual) |
| **Every Noise at Once** | Validação: listas de artistas representativos por gênero | Playlists e artistas (consulta manual) |
| **Million Song Dataset** | Propagação: ano, país e coordenadas de 1 milhão de músicas | Base pública (download + processamento) |

A implementação será feita na **Fase 2.5 (Enriquecimento de Dados)**, após a conclusão da API (Fase 3).

## Alternativas consideradas

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **Manter apenas Google Trends** | Já implementado | Dados insuficientes (apenas 7 registros) |
| **Radiooooo.com** | API disponível, dados curados | API privada em Ruby, sem suporte oficial |
| **Spotify Charts** | Popularidade atual | Sem dados históricos anteriores a 2015 |
| **Million Song Dataset** | Cobertura 1922–2011, gratuito | 280 GB (subconjunto de 1.8 GB disponível), requer pré-processamento |

## Consequências

**Positivas:**
- Cobertura temporal contínua de 1922 a 2011, preenchendo o vazio entre origens históricas e Google Trends
- Dados de localização precisos (country_code, latitude, longitude) para cada faixa
- Subconjunto de 1.8 GB (10.000 músicas) viável para processamento local

**Negativas:**
- Requer download e pré-processamento de arquivos HDF5
- A associação artista→gênero depende de metadados do próprio MSD (tags MusicBrainz)
- Curadoria manual adicional para filtrar falsos positivos
- Aumenta a complexidade do pipeline de dados
