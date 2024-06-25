# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

EXPOSE 8000

# Запускаем приложение
CMD ["gunicorn", "--bind", "127.0.0.1:8000", "MelodyGuide2.wsgi:application"]
