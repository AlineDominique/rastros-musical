# ADR 002: Seleção do Ruff para Linting e Formatação

## Status
Aceito

## Contexto
Para garantir alta qualidade de código e consistência no projeto **Rastros Musical**, precisávamos de um conjunto de ferramentas para linting (análise estática) e formatação. Tradicionalmente, o ecossistema Python utiliza uma combinação de várias ferramentas como Flake8, Black, isort e bandit.

No entanto, gerenciar múltiplas ferramentas aumenta:
1. A complexidade de configuração (múltiplos arquivos como `.flake8`, `pyproject.toml`, etc.).
2. O tempo de execução do CI/CD.
3. O potencial de conflitos entre o formatador e o linter.

## Decisão
Decidimos usar o **Ruff** como a ferramenta unificada tanto para linting quanto para formatação.

## Opções Consultadas
*   **Black + Flake8 + isort:** O padrão tradicional da indústria. Muito confiável, mas lento e requer o gerenciamento de três configurações de ferramentas separadas.
*   **Pylint:** Extremamente minucioso, mas significativamente mais lento e frequentemente produz um alto volume de falsos positivos que exigem supressão manual.
*   **Ruff:** Um linter e formatador moderno e extremamente rápido (escrito em Rust) que substitui Flake8, isort, Black e dezenas de outros plugins.

## Consequências
### Positivas
*   **Velocidade:** O Ruff é de 10x a 100x mais rápido que as ferramentas tradicionais, fornecendo feedback quase instantâneo durante o desenvolvimento e reduzindo os custos de CI/CD.
*   **Configuração Unificada:** Todas as regras (linting, ordenação de imports, formatação) são gerenciadas em um único arquivo `pyproject.toml`.
*   **Correções Integradas:** O Ruff pode corrigir automaticamente muitos erros comuns (como imports não utilizados), o que acelera o desenvolvimento.
*   **Padrões Modernos:** Suporta nativamente as últimas funcionalidades e melhores práticas do Python 3.13.

### Negativas
*   **Maturidade do Ecossistema:** Embora muito popular e estável, é mais recente que o Black ou o Flake8. No entanto, já é adotado por grandes projetos como FastAPI, Pandas e SciPy.

### Padrões de Documentação
*   **Idioma:** Todos os comentários de código, docstrings e mensagens de commit devem ser em **Inglês**.
*   **Formato:** Seguimos o **Google Python Style Guide** para docstrings.
*   **Execução:** O Ruff (pydocstyle) está configurado para validar a presença e a formatação das docstrings.

## Referências
* [Documentação do Ruff](https://docs.astral.sh/ruff/)
* [Transição do FastAPI para o Ruff](https://github.com/fastapi/fastapi/pull/10313)