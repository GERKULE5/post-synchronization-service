from typing import Dict
from services.vk.publish import Publisher

class MessageHandler:
    def __init__(self, publisher: Publisher, producer = None):
        self.publisher = publisher
        self.producer = producer
    
    async def handle(self, message: Dict):
        print(message)
        print('start handling')
        platform_type = message.get("platform_type")
        event_type = message.get("event_type")
        title = message.get("title")
        content = message.get("content")
        id = message.get('id')
        executor_id = message.get('executorId')
        post_id = message.get('vk_post_id')
        vk_group_ids = message.get("vk_group_ids")
        isPinned = message.get("isPinned")
        text = f"{title}\n{content}"

        if platform_type and event_type and vk_group_ids:
            if 'vk' in platform_type:
                if event_type == 'UPLOAD':
                    for group_id in vk_group_ids: 
                        post = await self.publisher.uploadPost(id, group_id, text)
                        print(post)
                        if isPinned is True:
                            await self.publisher.pinPost(group_id, post.get('post_id'))

                        await self.producer.send('posts.reply', {'executor_id': executor_id, 'news_id': id, 'post_id': post['post_id'], 'status': 'uploaded'})
                
                if event_type == 'EDIT':
                    for group_id in vk_group_ids:
                        post = await self.publisher.editPost(id, group_id, post_id, text)
                        if post:
                            await self.producer.send('posts.reply', {'executor_id': executor_id, 'news_id': id, 'post_id': post['post_id'], 'status': 'edited'})

                
                if event_type == 'DELETE':
                    for group_id in vk_group_ids:
                        post = await self.publisher.deletePost(group_id, post_id)
                        if post: 
                            await self.producer.send('posts.reply', {'executor_id': executor_id, 'news_id': id, 'status': 'deleted'})

                if event_type == 'RESTORE': 
                    for group_id in vk_group_ids:
                        post = await self.publisher.restorePost(group_id, post_id)
                        if post:
                            await self.producer.send('posts.reply', {'executor_id': executor_id, 'news_id': id, 'status': 'restored'})
                
                if event_type == 'PIN':
                    await self.publisher.pinPost(group_id, post_id)

                if event_type == 'SYNC':
                    print('SYNC is handled')

                if event_type == 'FETCH':
                    # Calls metho users.get(ids = None)
                    # Calls method groups.get(user_id) 
                    user = await self.publisher.get_user()
                    await self.get_groups(user[0]['id'])
                    print('FETCH is handled')
        