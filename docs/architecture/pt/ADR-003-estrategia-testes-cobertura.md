# ADR 003: Estratégia de Testes e Cobertura

## Status
Aceito

## Contexto
À medida que o projeto **Rastros Musical** cresce, garantir que novas funcionalidades não quebrem a lógica existente é crítico. Precisamos de uma forma de quantificar quanto da nossa lógica de aplicação é realmente exercitada por nossa suíte de testes.

## Decisão
Utilizaremos o **Pytest** com o plugin **pytest-cov** para fortalecer uma cultura de testes.
*   **Testes Unitários:** Cobrirão schemas e funções utilitárias.
*   **Testes de Integração:** Cobrirão endpoints da API e migrações do DuckDB.

## Consequências
### Positivas
*   **Visibilidade:** Desenvolvedores podem ver exatamente quais linhas de código estão sem testes.
*   **Confiança:** Alta cobertura (visando >80%) proporciona confiança para refatorações frequentes.
*   **Barreira de Qualidade (Quality Gate):** Podemos configurar o CI/CD futuramente para falhar caso a cobertura caia abaixo de um certo limite.

### Negativas
*   **Manutenção:** Testes precisam ser atualizados juntamente com o código.
*   **Falsa Segurança:** 100% de cobertura não significa 0% de bugs, apenas que o código foi executado.