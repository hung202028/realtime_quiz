# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app .
COPY .env .
COPY requirements.txt .

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]