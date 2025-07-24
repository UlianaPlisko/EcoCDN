FROM python:3.9-slim

# Рабочая директория
WORKDIR /app

# Копируем приложение и папку с книгами
COPY server.py /app/server.py
COPY books /app/books

# Устанавливаем зависимости
RUN pip install --no-cache-dir flask

# Открываем порт
EXPOSE 5000

# Запускаем сервер
CMD ["python", "server.py"]