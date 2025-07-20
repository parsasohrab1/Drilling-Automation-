import json
from kafka import KafkaConsumer

# تنظیمات Kafka
KAFKA_BROKER = 'kafka:9092'
TOPIC_NAME = 'sensor-data'


def create_consumer():
    """ایجاد یک Kafka Consumer"""
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )


def main():
    consumer = create_consumer()
    print("Consumer started. Waiting for sensor data...")

    try:
        for message in consumer:
            data = message.value
            print(f"Received: {data}")
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()