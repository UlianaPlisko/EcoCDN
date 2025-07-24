FROM python:3.9-slim
WORKDIR /app

COPY controller.py /app
RUN pip install --no-cache-dir flask

EXPOSE 5005
CMD ["python", "controller.py"]