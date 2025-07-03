FROM python:3.12-alpine

WORKDIR /app

# Pip'i güncelle
RUN pip install --upgrade pip

# Requirements'ı kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Healthcheck ekle
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import app; print('OK')" || exit 1

CMD ["python", "server.py"]