import os

from flask import Flask
from flask_cors import CORS
from app.kafka_config import get_kafka_consumer, get_kafka_producer, is_kafka_enabled, wait_for_kafka
from app.routes import initialize_routes

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Kafka initialization
    with app.app_context():
        wait_for_kafka()
        app.config['KAFKA_ENABLED'] = is_kafka_enabled()
        app.config['KAFKA_PRODUCER'] = get_kafka_producer()
        app.config['KAFKA_CONSUMER'] = get_kafka_consumer()

        initialize_routes(app)

    return app
