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

CMD ["python", "server.py"]