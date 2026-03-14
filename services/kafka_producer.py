from aiokafka import AIOKafkaProducer
from typing import Dict, Optional
import json
from .kafka_base import KafkaBase

class KafkaProducer(KafkaBase):
    def __init__(self, url: str):
        super().__init__(url)
        self.producer: Optional[AIOKafkaProducer] = None
    
    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.url,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks=1
        )
        await self.producer.start()
        self._client = self.producer
        print('Producer started')
    
    async def send(self, topic: str, message: Dict):
        if not self.producer:
            raise RuntimeError("Producer not started")
        
        result = await self.producer.send_and_wait(topic, message)
        print(f"Sent to {topic}: {message}")
        return result
