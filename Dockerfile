# Usando a versão estável mais recente do Python
FROM python:3.13-slim

# Definir variáveis de ambiente para o Python não gerar arquivos .pyc e não bufferizar logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências do sistema necessárias para o DuckDB e extensões espaciais
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Atualizar o pip antes de instalar os pacotes
RUN pip install --upgrade pip

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# O código será montado via volume no Docker Compose para facilitar o desenvolvimento
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]