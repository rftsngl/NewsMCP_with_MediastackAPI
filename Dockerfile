FROM python:3.12-alpine

WORKDIR /app

# Pip'i güncelle
RUN pip install --upgrade pip

# Requirements'ı kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default port - Smithery will override with PORT env var
ENV PORT=8000
EXPOSE $PORT

# Healthcheck for FastMCP HTTP endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import requests; import os; requests.post('http://localhost:'+str(os.getenv('PORT', '8000'))+'/mcp', json={'jsonrpc': '2.0', 'method': 'ping', 'id': 1}, timeout=5)" || exit 1

CMD ["python", "server.py"]