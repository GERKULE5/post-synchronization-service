from aiokafka import AIOKafkaConsumer
from typing import Optional, Callable, Awaitable
import json
from .kafka_base import KafkaBase

class KafkaConsumer(KafkaBase):
    def __init__(self, url: str, topic: str, group_id: str = None):
        super().__init__(url)
        self.topic = topic
        self.group_id = group_id or f"consumer-{topic}"
        self.consumer: Optional[AIOKafkaConsumer] = None
        self.running = False
    
    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.url,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            group_id=self.group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        await self.consumer.start()
        self._client = self.consumer
        self.running = True
        print(f'Consumer started for topic: {self.topic}')
    
    async def consume(self, callback: Callable[[dict], Awaitable[None]]):
        try:
            async for msg in self.consumer:
                if not self.running:
                    break
                print(f"Received: {msg.value}")
                await callback(msg.value)
        except Exception as e:
            print(f"Consume error: {e}")
    
    async def stop(self):
        self.running = False
        await super().stop()
        