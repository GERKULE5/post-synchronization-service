from typing import Dict
from services.vk.publish import Publisher

class MessageHandler:
    def __init__(self, publisher: Publisher):
        self.publisher = publisher
    
    async def handle(self, message: Dict):
        print(message)
        print('start handling')
        platform_type = message.get("platform_type")
        event_type = message.get("event_type")
        title = message.get("title")
        content = message.get("content")
        vk_group_ids = message.get("vk_group_ids")
        message = f"{title}\n{content}"

        if platform_type and event_type and vk_group_ids:
            if 'vk' in platform_type:
                if event_type == 'upload':
                    for group_id in vk_group_ids: 
                        await self.publisher.uploadPost(group_id, message)
        