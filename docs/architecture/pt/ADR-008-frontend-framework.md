# ADR 008: Framework de Frontend e Biblioteca de Visualização

## Status
Proposto

## Contexto
O projeto **Rastros Musical** exige uma interface capaz de renderizar grandes volumes de dados geoespaciais e séries temporais de forma fluida. Precisamos escolher tecnologias que suportem alta performance e integração com o ecossistema Docker/FastAPI.

## Decisão
Utilizaremos **React** como framework de interface e **Deck.gl** como biblioteca de visualização de dados geoespaciais.

## Justificativa
1. **Performance via GPU**: O Deck.gl utiliza WebGL para renderizar milhares de pontos e arcos sem sobrecarregar a CPU, garantindo um MVP robusto.
2. **Ecossistema e Mercado**: O React possui a maior comunidade e suporte para bibliotecas de mapas complexos, além de ser altamente valorizado no mercado de tecnologia.
3. **Compatibilidade com Docker**: Ambos funcionam de forma otimizada em ambientes containerizados, facilitando o CI/CD.
4. **Data-Driven**: A estrutura do Deck.gl baseada em camadas (layers) conversa diretamente com a nossa modelagem de dados Medallion.

## Consequências
* **Positivas**: Interface de alta fidelidade e escalabilidade para grandes datasets musicais.
* **Negativas**: Curva de aprendizado inicial maior do que soluções simples como HTML puro ou HTMX.