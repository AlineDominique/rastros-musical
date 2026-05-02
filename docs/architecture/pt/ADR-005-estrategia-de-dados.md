# ADR 005: Data Strategy with MusicBrainz / Estratégia de Dados com MusicBrainz

## Status
Aceito

## Contexto

O objetivo do mapa é mostrar a evolução geográfica e temporal. Precisamos de uma fonte que ofereça metadados históricos (datas de início) e localização precisa (países e cidades) sem depender de algoritmos de popularidade comercial.

## Decisão

Usaremos o **MusicBrainz** como nossa **única fonte de verdade** para este MVP:
*   **Dados Geográficos:** Utilizaremos os campos `area` e `coordinates` para alimentar o mapa.
*   **Dados Temporais:** Focaremos no campo `begin-date` para construir a linha do tempo.
*   **Motor de Dados:** O **DuckDB** fará a ingestão desses dados para permitir consultas rápidas de agregação por continente.

## Consequências
### Positivas
* **Integridade:** Dados históricos verificados pela comunidade MusicBrainz.
* **Performance:** Consultas locais no DuckDB eliminam a latência de APIs externas.
* **Foco:** Remover a API do Spotify reduz a complexidade de autenticação e foca na engenharia de dados.

### Negativas
* **Volume de Dados:** O MusicBrainz é vasto e exige uma limpeza inicial rigorosa para os eixos América Latina e Ásia.