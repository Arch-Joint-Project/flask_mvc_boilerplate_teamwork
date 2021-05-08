import os
import json
from kafka import KafkaProducer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS.split("|")


def json_serializer(data):
    return json.dumps(data).encode("UTF-8")


def get_partition(key, all, available):
    return 0


producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=json_serializer,
    partitioner=get_partition,
)
