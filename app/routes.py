from flask import jsonify, request, current_app
from confluent_kafka import KafkaException

from app import is_kafka_enabled


def initialize_routes(app):
    @app.route('/healthcheck', methods=['GET'])
    def healthcheck():
        return jsonify(
            {
                "status": "healthy",
                "kafka_enabled": is_kafka_enabled(),
                "kafka_producer_initialized": bool(current_app.config.get('KAFKA_PRODUCER')),
                "kafka_consumer_initialized": bool(current_app.config.get('KAFKA_CONSUMER')),
            }
        ), 200

    @app.route('/users', methods=['POST'])
    def create_user():
        return jsonify({"status": "created"}), 201

    @app.route('/produce', methods=['POST'])
    def produce_message():
        if not is_kafka_enabled():
            return jsonify({'error': 'Kafka is not enabled'}), 500

        kafka_producer = current_app.config.get('KAFKA_PRODUCER')
        if not kafka_producer:
            return jsonify({'error': 'Kafka producer is not initialized'}), 500

        data = request.json
        topic = data.get('topic')
        message = data.get('message')

        if not topic or not message:
            return jsonify({'error': 'Topic and message are required'}), 400

        kafka_producer.produce(topic, message)
        kafka_producer.flush()

        return jsonify({'status': 'Message sent to Kafka', 'topic': topic, 'message': message}), 200

    @app.route('/consume', methods=['GET'])
    def consume_message():
        if is_kafka_enabled():
            return jsonify({'error': 'Kafka is not enabled'}), 400

        kafka_consumer = current_app.config.get('KAFKA_CONSUMER')

        if not kafka_consumer:
            return jsonify({'error': 'Kafka consumer is not initialized'}), 500

        kafka_consumer.subscribe(['Test Topic'])

        messages = []
        try:
            for _ in range(10):
                msg = kafka_consumer.poll(timeout=1.0)
                if msg is None:
                    break
                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        break
                    else:
                        raise KafkaException(msg.error())
                messages.append(msg.value().decode('utf-8'))
        except KafkaException as e:
            return jsonify({'error': str(e)}), 500

        return jsonify({'messages': messages}), 200
