FROM python:3.9-slim
WORKDIR /app

COPY simulate.py /app
RUN pip install --no-cache-dir requests

# По умолчанию запрашиваем book1.pdf
CMD ["python", "simulate.py", "book1.pdf"]