import sys
import types
import asyncio
import json
import importlib.util
import os


class DummyMessage:
    def __init__(self, body: bytes):
        self.body = body

    class _cm:
        async def __aenter__(self):
            return None

        async def __aexit__(self, exc_type, exc, tb):
            return False

    def process(self):
        return DummyMessage._cm()


def test_handle_message_calls_process_document():
    # Provide a fake `app.services.document_processor` module before loading file
    fake_mod = types.ModuleType("app.services.document_processor")

    called = {"count": 0, "payload": None}

    async def fake_process_document(payload):
        called["count"] += 1
        called["payload"] = payload

    fake_mod.process_document = fake_process_document
    sys.modules["app.services.document_processor"] = fake_mod

    # Also ensure shared.messaging.rabbit_mq does not import `app.core.config`
    fake_rmq = types.ModuleType("shared.messaging.rabbit_mq")

    def get_rabbitmq_url():
        return "amqp://guest:guest@localhost:5672/"

    fake_rmq.get_rabbitmq_url = get_rabbitmq_url
    sys.modules["shared.messaging.rabbit_mq"] = fake_rmq

    # Load the consumer module directly from file to avoid package import issues
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    path = os.path.join(base, "worker", "app", "consumers", "document_consumer.py")
    spec = importlib.util.spec_from_file_location("worker_document_consumer", path)
    consumer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(consumer)

    payload = {"document_id": "123", "source": "upload"}
    message = DummyMessage(json.dumps(payload).encode())

    asyncio.get_event_loop().run_until_complete(consumer.handle_message(message))

    assert called["count"] == 1
    assert called["payload"] == payload
