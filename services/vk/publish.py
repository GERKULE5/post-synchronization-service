from vk_api import VkApi
from vk_api.upload import VkUpload



class Publisher:
    def __init__(self, token: str, producer=None):
        self.token = token
        self.producer = producer
        self.vk_session = None
        self.vk = None
        self.upload = None
    
    async def initialize(self) -> bool:
        try:
            self.vk_session = VkApi(token=self.token)
            self.vk = self.vk_session.get_api()
            self.upload = VkUpload(self.vk_session)

            print('Groups connected')
            return True
        
        except Exception as e:
            print(e)
            return False
        
    def get_owner_id(self, group_id: int) -> int:
        return -int(group_id)

    async def uploadPost(self, group_id: int, message: str):
        print('try to upload post')
        try:
            post = self.vk.wall.post(owner_id=self.get_owner_id(group_id), message=message, from_group=1)
            post_id = post['post_id']
            print(f'post uploaded: {post_id}')
            await self.producer.send('posts', {'status': 'uploaded', 'post_id': post_id})
            return post
            
        except Exception as e:
            print(e)
            return None, e

    async def deletePost(self, group_id: int, post_id: int):
        print('try to delete post')
        try:
            post = self.vk.wall.delete(owner_id=self.get_owner_id(group_id) , post_id=post_id)
            print(f'post deleted: {post_id}')
            await self.producer.send('posts', {'status': 'deleted','post_id': post_id, 'code': post})
            return post
        
        except Exception as e:
            print(e)
            return None, e        

    async def editPost(self, group_id: int, post_id: int, message: str):
        print('try to edit post')
        try: 
            post = self.vk.wall.edit(owner_id=self.get_owner_id(group_id), post_id=post_id, message=message)
            post_id = post['post_id']
            print(f'post edited: {post_id}')
            await self.producer.send('posts', {'status': 'edited','post_id': post_id})
            return post
        
        except Exception as e:
            print(e)
            return None, e
