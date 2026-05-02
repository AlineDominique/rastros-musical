# ADR 004: Clean Code and TDD Standards
## Status
Accepted

## Context
For a project tracking the historical evolution of musical genres, **data precision is non-negotiable**. We need to ensure the business logic is readable, auditable, and resilient to changes, especially when dealing with the complexity of multiple countries across Latin America and Asia.

## Decision
We will adopt **TDD (Test-Driven Development)** and **Clean Code** principles as core development pillars:
*   **TDD Cycle:** No filtering or transformation logic will be written without a failing unit test first (*Red-Green-Refactor*).
*   **Self-Documenting Code:** We will prioritize semantic naming and Single Responsibility Principle (SRP).
*   **Strict Typing:** We will use *Type Hinting* and *Pydantic* to ensure geographical and temporal data integrity.

## Consequences
### Positive
*   **Maintainability:** Code will be easy to understand even months after it was written.
*   **Reliability:** Logic for cross-referencing data will be mathematically validated by tests.
*   **Debt Reduction:** Continuous refactoring prevents the system from becoming a "black box."

### Negative
*   **Initial Velocity:** The start of the project is slower as the focus is on structural quality.