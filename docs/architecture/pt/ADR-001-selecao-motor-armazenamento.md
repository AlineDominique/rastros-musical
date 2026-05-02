# ADR 001: Seleção do DuckDB como Motor de Armazenamento Analítico

## Status
Aceito

## Contexto
O projeto **Rastros Musical** exige um motor robusto para processar e analisar dados de propagação musical entre a América Latina e a Ásia. Os dados incluem coordenadas geográficas, séries temporais e métricas de popularidade.

Precisávamos de uma solução que:
1. Suportasse consultas analíticas de alta performance (OLAP).
2. Lidasse com dados espaciais/geográficos de forma eficiente.
3. Fosse fácil de configurar em ambientes de desenvolvimento e CI/CD sem a sobrecarga de um servidor de banco de dados dedicado.
4. Integrasse perfeitamente com Python 3.13 e o ecossistema moderno de dados (Pandas/Polars).

## Decisão
Decidimos usar o **DuckDB** como o principal motor analítico, juntamente com sua **Extensão Espacial** oficial.

## Opções Consultadas
*   **PostgreSQL + PostGIS:** Robusto, mas requer o gerenciamento de um servidor/container de banco de dados separado, aumentando a complexidade da infraestrutura em um estágio inicial.
*   **SQLite:** Fácil de usar, mas carece de capacidades analíticas nativas de alta performance (armazenamento colunar) e possui suporte espacial limitado em comparação ao DuckDB.
*   **Pandas (Em memória):** Eficiente para escalas pequenas, mas carece de interface SQL para joins relacionais complexos e indexação espacial persistente.

## Consequências
### Positivas
*   **Performance:** O motor colunar do DuckDB é otimizado para os tipos de agregações que realizaremos (ex: popularidade média por região por ano).
*   **Simplicidade:** O banco de dados é armazenado em um único arquivo, tornando-o portátil e fácil de realizar backup ou versionamento, se necessário.
*   **Capacidades Espaciais:** A extensão Spatial permite realizar cálculos de "Pontos em Polígono" e distância diretamente via SQL.
*   **Integração:** Compatibilidade direta com FastAPI e Pydantic através da API Python.

### Negativas
*   **Concorrência:** O DuckDB é otimizado para cargas de trabalho de escrita única. Isso é aceitável para o nosso processo de ETL, mas deve ser gerenciado se escalarmos para múltiplos serviços de escrita simultânea.
*   **Persistência:** Como é um banco de dados in-process, devemos garantir que os volumes do Docker estejam configurados corretamente para evitar a perda de dados quando os containers forem destruídos.

## Referências
* [Documentação do DuckDB](https://duckdb.org/docs/)
* [Extensão Espacial do DuckDB](https://duckdb.org/docs/extensions/spatial)