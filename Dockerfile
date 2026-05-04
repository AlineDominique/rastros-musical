FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala o uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copia arquivos de dependência E o README (exigido pelo hatchling)
COPY pyproject.toml uv.lock README.md ./

# Instala dependências (produção + dev)
RUN uv sync --frozen --dev

# Copia o restante do código
COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]