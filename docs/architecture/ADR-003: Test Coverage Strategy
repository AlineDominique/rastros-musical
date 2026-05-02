# ADR 003: Testing and Coverage Strategy

## Status
Accepted

## Context
As the **Rastros Musical** project grows, ensuring that new features do not break existing logic is critical. We need a way to quantify how much of our application logic is actually exercised by our test suite.

## Decision
We will use **Pytest** with the **pytest-cov** plugin to enforce a testing culture. 
*   **Unit Tests:** Will cover schemas and utility functions.
*   **Integration Tests:** Will cover API endpoints and DuckDB migrations.

## Consequences
### Positive
*   **Visibility:** Developers can see exactly which lines of code are missing tests.
*   **Confidence:** High coverage (aiming for >80%) provides confidence for frequent refactoring.
*   **Quality Gate:** We can later configure CI/CD to fail if coverage drops below a certain threshold.

### Negative
*   **Maintenance:** Tests need to be updated alongside code.
*   **False Security:** 100% coverage doesn't mean 0% bugs, only that the code was executed.