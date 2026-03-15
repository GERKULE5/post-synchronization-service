import asyncio
from os import getenv
from dotenv import load_dotenv

from services.kafka_producer import KafkaProducer
from services.kafka_consumer import KafkaConsumer
from services.handlers.message_handler import MessageHandler

load_dotenv()


async def main():
    producer = KafkaProducer(url=getenv('KAFKA_URL'))
    consumer = KafkaConsumer(
        url=getenv('KAFKA_URL'),
        topic='posts',
        group_id='test-group'
    )
    
    handler = MessageHandler(producer)
    
    try:    
        await producer.start()
        await consumer.start()
        await consumer.consume(handler.handle)

        
    finally:
        await consumer.stop()
        await producer.stop()

if __name__ == '__main__':
    asyncio.run(main())
