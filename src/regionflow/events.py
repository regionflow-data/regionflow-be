from __future__ import annotations

import json
import os
from collections.abc import Iterable

from .pipeline import RegionSnapshot


def cache_snapshots(snapshots: Iterable[RegionSnapshot]) -> int:
    import redis

    client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
    count = 0
    for snapshot in snapshots:
        client.setex(f"regionflow:snapshot:{snapshot.region}", 900, json.dumps(snapshot.__dict__))
        count += 1
    return count


def publish_snapshots(snapshots: Iterable[RegionSnapshot]) -> int:
    import pika

    connection = pika.BlockingConnection(pika.URLParameters(os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672")))
    channel = connection.channel()
    channel.queue_declare(queue="regionflow.region.snapshots", durable=True)
    count = 0
    for snapshot in snapshots:
        channel.basic_publish(exchange="", routing_key="regionflow.region.snapshots", body=json.dumps(snapshot.__dict__))
        count += 1
    connection.close()
    return count
