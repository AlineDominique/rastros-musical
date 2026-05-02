# ADR 004: Padrões de Clean Code e TDD

## Status
Aceito

## Contexto
Para um projeto que rastreia a evolução histórica de gêneros musicais, a **precisão do dado é inegociável**. Precisamos garantir que a lógica de negócio seja legível, auditável e resistente a mudanças, especialmente ao lidar com a complexidade de múltiplos países da América Latina e Ásia.

## Decisão
Adotaremos o **TDD (Test-Driven Development)** e princípios de **Clean Code** como pilares de desenvolvimento:
*   **Ciclo TDD:** Nenhuma lógica de filtragem ou transformação será escrita sem um teste unitário que falhe primeiro (*Red-Green-Refactor*).
*   **Código Autodocumentado:** Priorizaremos nomes semânticos e o Princípio de Responsabilidade Única (SRP).
*   **Tipagem Estrita:** Usaremos *Type Hinting* e *Pydantic* para garantir a integridade dos dados geográficos e temporais.

## Consequências
### Positivas
* **Manutenibilidade:** O código será fácil de entender, mesmo meses após a escrita.
* **Confiabilidade:** A lógica de cruzamento de dados será validada matematicamente pelos testes.
* **Redução de Débito:** O refatoramento contínuo evita que o sistema se torne uma "caixa preta".

### Negativas
* **Velocidade Inicial:** O início do projeto é mais lento, pois o foco está na qualidade da estrutura.