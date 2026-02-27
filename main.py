import asyncio
from os import getenv
from dotenv import load_dotenv

from services.kafka_producer import KafkaProducer
from services.kafka_consumer import KafkaConsumer

from services.vk.publish import Publisher


load_dotenv()


async def handle_message(message):
    print(f"Got message: {message}")

async def main():
   
    producer = KafkaProducer(url=getenv('KAFKA_URL'))
    consumer = KafkaConsumer(
        url=getenv('KAFKA_URL'),
        topic='posts',
        group_id='test-group'
    )

    group_id = getenv("VK_GROUP_ID")

    publisher = Publisher(
        token=getenv('ACCESS_TOKEN'),
        producer=producer)
    
    try:
      
        await producer.start()
        await consumer.start()
        await publisher.initialize()
        
        #await publisher.uploadPost(group_id, "post ")
        #await publisher.deletePost(group_id, post_id=42)
        #await publisher.editPost(group_id, post_id=4, message="edited")
        #await publisher.restorePost(group_id, post_id=42)
        await publisher.getPosts(group_id=group_id, count=1)
        
        await consumer.consume(handle_message)    
        
    finally:
     
        await consumer.stop()
        await producer.stop()

if __name__ == '__main__':
    asyncio.run(main())
