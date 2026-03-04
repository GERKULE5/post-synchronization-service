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
        id = message.get('id')
        post_id = message.get('vk_post_id')
        vk_group_ids = message.get("vk_group_ids")
        isPinned = message.get("isPinned")
        message = f"{title}\n{content}"

        if platform_type and event_type and vk_group_ids:
            if 'vk' in platform_type:
                if event_type == 'UPLOAD':
                    for group_id in vk_group_ids: 
                        post = await self.publisher.uploadPost(id, group_id, message)
                        if isPinned is True:
                            await self.publisher.pinPost(group_id,post.post_id)
                
                if event_type == 'EDIT':
                    await self.publisher.editPost(group_id, post_id, message)
                
                if event_type == 'DELETE':
                    await self.publisher.deletePost(group_id, post_id)

                if event_type == 'RESTORE': 
                    await self.publisher.restorePost(group_id, post_id)
                
                if event_type == 'PIN':
                    await self.publisher.pinPost(group_id, post_id)
                        
        