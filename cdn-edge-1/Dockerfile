FROM python:3.9-slim
WORKDIR /app

COPY edge-node.py /app
RUN pip install --no-cache-dir flask requests

EXPOSE 5001
CMD ["python", "edge-node.py"]
