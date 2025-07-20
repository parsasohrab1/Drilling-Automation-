FROM python:3.9-slim

WORKDIR /app

COPY producer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY producer/sensor_producer.py .

CMD ["python", "sensor_producer.py"]ش