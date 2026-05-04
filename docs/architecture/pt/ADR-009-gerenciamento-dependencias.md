# ADR-009: Gerenciamento de dependências com `pyproject.toml` e `uv`

**Status:** Aceito  
**Data:** 2026-05-04  

---

## Contexto

O projeto usava `requirements.txt` e `requirements-dev.txt` com `pip`. O ecossistema Python consolidou o `pyproject.toml` (PEP 621) como padrão e o `uv` como gerenciador rápido e determinístico.

## Decisão

Substituímos os arquivos `requirements.txt` e `requirements-dev.txt` por dependências declaradas diretamente no `pyproject.toml`, utilizando o `uv` como gerenciador de pacotes e ambientes. O `pyproject.toml` passa a concentrar:

- Metadados do projeto (`[project]`: nome, versão, autor, licença, URLs)
- Dependências de produção (`[project.dependencies]`)
- Dependências de desenvolvimento (`[project.optional-dependencies] dev`)
- Configurações de build (`[build-system]` com hatchling)
- Configuração de destino de build (`[tool.hatch.build.targets.wheel]`)
- Configurações de ferramentas (Ruff, pytest, coverage)

O `uv.lock` substitui o `requirements.txt` congelado como fonte de verdade para builds reproduzíveis.

## Alternativas consideradas

| Alternativa | Velocidade | Lock file | PEP 621 | Integração Ruff | Curva de aprendizado |
|-------------|:----------:|:---------:|:-------:|:---------------:|:--------------------:|
| `pip` + `pip-tools` | Lenta |  Sim |  Não |  Não | Baixa |
| Poetry | Média |  Sim |  Não (próprio) |  Não | Média |
| PDM | Média |  Sim |  Sim |  Não | Média |
| **uv** | **Muito rápida** |  Sim |  Sim |  Sim | Baixa |


## Consequências

**Positivas:**
- Um arquivo único: `pyproject.toml` substitui múltiplos arquivos de dependências
- `uv.lock` garante builds idempotentes em qualquer ambiente
- Instalação até 10x mais rápida que `pip` no Docker e CI

**Negativas:**
- `uv` precisa estar disponível no ambiente (local ou Docker)
- Hatchling exige `[tool.hatch.build.targets.wheel]` e valida `readme`


## Problemas resolvidos

Os erros encontrados e suas soluções estão detalhados no diário de aprendizado:

- [uv + pyproject.toml — 04 Mai 2026](../../learnings/2026-05-04-uv-pyproject.md)


**Links**
- [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [uv documentation](https://docs.astral.sh/uv/)
- [Hatchling build configuration](https://hatch.pypa.io/latest/config/build/)