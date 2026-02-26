from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from typing import Dict, Optional
import json

class KafkaService:
    def __init__(self, url: str, topic: str):
        self.url = url
        self.topic = topic
        self.producer: Optional[AIOKafkaProducer] = None
        self.consumer: Optional[AIOKafkaConsumer] = None

    async def start(self):
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.url,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks=1
            )

            self.consumer = AIOKafkaConsumer(
                self.topic, 
                bootstrap_servers=self.url,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v else None
            )
                
            await self.producer.start()
            await self.consumer.start()
        except Exception as e:
            print(e)
            raise

    async def send(self, topic: str, message: Dict):

        if not self.producer:
            raise RuntimeError("Producer not started")
        
        result_send = await self.producer.send_and_wait(topic, message)

        print("Flushing producer...")
        await self.producer.flush()
        print("Flush completed")

        print(result_send)
        print(f"Message sent to {topic}: {message}")

    async def stop(self):
        if self.consumer:
            try:
                await self.consumer.stop()
            except:
                pass
        
        if self.producer:
            try:
                await self.producer.stop()
            except:
                pass
