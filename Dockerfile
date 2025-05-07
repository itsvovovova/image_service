# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь контейнера
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска приложения через uvicorn
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}