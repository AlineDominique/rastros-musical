# ADR 006: Modelagem de Dados e Fluxo Analítico

## Status
Proposto

## Contexto
O sistema deve transformar metadados brutos do MusicBrainz em insights sobre a propagação musical entre América Latina e Ásia.

## Decisão
Utilizaremos uma arquitetura de camadas (Medallion) dentro do **DuckDB**:
1. **Bronze (Raw)**: Ingestão direta da API/Dump.
2. **Silver (Trusted)**: Dados limpos, tipados e com normalização geográfica.
3. **Gold (Refined)**: Agregações temporais prontas para a API.

## Diagrama de Fluxo


## Justificativa
Esta abordagem garante que a **precisão do dado seja inegociável** e permite auditoria em cada etapa do processamento analítico.

## Consequências
* **Positivas**: Separação clara entre extração e lógica de negócio.
* **Negativas**: Requer mais armazenamento em disco para manter as camadas intermediárias.