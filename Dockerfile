# Dockerfile generated on: 2025-07-02T17:48:35.112706Z
FROM python:3.11-slim
# Project Type: python

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
