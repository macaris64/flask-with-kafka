import time

from confluent_kafka import Producer, Consumer
import os

producer = None
consumer = None

def get_kafka_producer():
    global producer
    if producer is None:
        producer_config = {
            'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
            'message.max.bytes': int(os.environ.get('KAFKA_MESSAGE_MAX_BYTES', 100000000)),
        }
        producer = Producer(producer_config)

    return producer

def get_kafka_consumer():
    global consumer
    if consumer is None:
        consumer_config = {
            'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
            'group.id': 'flask_app_group',
            'auto.offset.reset': 'earliest',
            'fetch.message.max.bytes': int(os.environ.get('KAFKA_REPLICA_FETCH_MAX_BYTES', 100000000)),
        }
        consumer = Consumer(consumer_config)
    return consumer

def is_kafka_enabled():
    return os.environ.get("ENABLE_KAFKA", "0") == "1"

def wait_for_kafka():
    retries = 5
    while retries > 0 and is_kafka_enabled():
        try:
            producer = Producer({'bootstrap.servers': 'kafka:9092'})
            producer.list_topics(timeout=5)
            print("Kafka connection successful.")
            return
        except Exception as e:
            print(f"Kafka connection not success.: {e}. Retrying...")
            retries -= 1
            time.sleep(5)
    raise Exception("Kafka connection not success.")
