# ADR 005: Estrutura de Repositório (Monorepo)

## Status
Proposto

## Contexto
O projeto **Rastros Musical** consiste em uma API de dados analíticos e uma interface de visualização. Precisamos decidir entre separar esses componentes em repositórios distintos ou mantê-los juntos.

## Decisão
Adotaremos a estratégia de **Monorepo**. O código do Backend residirá em `/app` e o Frontend em `/web`.

## Justificativa
1. **Sincronia de Contratos**: Garante que mudanças nos Schemas de dados (Pydantic) e na interface ocorram simultaneamente.
2. **Simplicidade de Deploy**: Facilita a configuração de CI/CD gratuito (Vercel/Render) em um único fluxo de trabalho.
3. **Visão Estratégica**: Centraliza a governança (ADRs, TODO.md) e o histórico de evolução do ciclo de vida do dado.

## Consequências
* **Positivas**: Facilidade de refatoração cross-stack e gestão única de issues.
* **Negativas**: O tamanho do repositório cresce mais rápido, mas é irrelevante para a escala de um MVP.