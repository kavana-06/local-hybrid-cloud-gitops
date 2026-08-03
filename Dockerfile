FROM python:3.12-slim

WORKDIR /app

COPY app/monitor.py .

RUN pip install --no-cache-dir psutil

RUN mkdir -p /app/logs

CMD ["python", "monitor.py"]
