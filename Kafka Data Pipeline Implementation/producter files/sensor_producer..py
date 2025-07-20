import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

# تنظیمات Kafka
KAFKA_BROKER = 'kafka:9092'
TOPIC_NAME = 'sensor-data'

# تنظیمات شبیه‌سازی حسگر
SENSOR_IDS = ['sensor-1', 'sensor-2', 'sensor-3']
SENSOR_TYPES = ['temperature', 'humidity', 'pressure']


def generate_sensor_data():
    """تولید داده‌های شبیه‌سازی شده حسگر"""
    return {
        'sensor_id': random.choice(SENSOR_IDS),
        'type': random.choice(SENSOR_TYPES),
        'value': round(random.uniform(0, 100), 2),
        'timestamp': datetime.utcnow().isoformat()
    }


def create_producer():
    """ایجاد یک Kafka Producer"""
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


def main():
    producer = create_producer()
    print("Producer started. Sending sensor data...")

    try:
        while True:
            data = generate_sensor_data()
            producer.send(TOPIC_NAME, value=data)
            print(f"Sent: {data}")
            time.sleep(random.uniform(0.5, 2))
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()