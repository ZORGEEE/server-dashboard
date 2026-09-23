FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Устанавливаем Gunicorn
RUN pip install gunicorn

EXPOSE 8095

# Запускаем через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8095", "app:app"]
