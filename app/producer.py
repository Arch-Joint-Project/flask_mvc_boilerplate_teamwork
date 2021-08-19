import os
import json

import loguru
from kafka import KafkaProducer
from kafka.errors import KafkaError

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", default="localhost:90")
bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS.split("|")


def json_serializer(data):
    return json.dumps(data).encode("UTF-8")


def get_partition(key, all, available):
    return 0


def publish_to_kafka(topic, value):
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=json_serializer,
        partitioner=get_partition,
    )
    try:
        producer.send(topic=topic, value=value)
        return True
    except KafkaError as e:
        loguru.Logger.error(
            f"Failed to publish record on to Kafka broker with error {e}"
        )
        return False
