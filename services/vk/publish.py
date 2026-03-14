from vk_api import VkApi
from vk_api.upload import VkUpload
from typing import Optional



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

    async def uploadPost(self, id: int, group_id: int, message: str):
        print('try to upload post')
        try:
            post = self.vk.wall.post(owner_id=self.get_owner_id(group_id), message=message, from_group=1)
            return post
            
        except Exception as e:
            print(e)
            return None, e

    async def deletePost(self, id: int, group_id: int, post_id: int):
        print('try to delete post')
        try:
            post = self.vk.wall.delete(owner_id=self.get_owner_id(group_id) , post_id=post_id)
            print('post uploaded')
            return post
        
        except Exception as e:
            print(e)
            return None, e        

    async def editPost(self, id: int, group_id: int, post_id: int, message: str):
        print('try to edit post')
        try: 
            post = self.vk.wall.edit(owner_id=self.get_owner_id(group_id), post_id=post_id, message=message)
            print('post edited')
            return post
        
        except Exception as e:
            print(e)
            return None, e
        
    async def restorePost(self, group_id: int, post_id: int):
        print(f'try to restore post {post_id}')
        try: 
            post = self.vk.wall.restore(owner_id=self.get_owner_id(group_id), post_id=post_id)
            print('post restroed')
            return post
        
        except Exception as e:
            print(e)
            return None, e
    
    async def pinPost(self, group_id: int, post_id: int):
        print('try to pin post')
        try:
            post = self.vk.wall.pin(owner_id=self.get_owner_id(group_id), post_id=post_id)
            print('post pinned')
            return post
        except Exception as e:
            print(e)
            return None, e
        
    async def getPosts(self, group_id: int, count: int):
        
        # Метод vk.wall.get возвращает:
        # {
        #     'count': 12, 
        #     'items': [{
        #         'inner_type': 'wall_wallpost', 
        #         'can_edit': 1, 
        #         'created_by': 876482061, 
        #         'can_delete': 1, 
        #         'can_pin': 1, 
        #         'comments': {
        #             'can_post': 1, 
        #             'can_close': 1, 
        #             'count': 0, 
        #             'groups_can_post': True
        #         }, 
        #         'marked_as_ads': 0, 
        #         'zoom_text': True, 
        #         'hash': 'fpnTVoB4cfig4T5AXBZeIymsNhip', 
        #         'type': 'post', 
        #         'push_subscription': {
        #             'is_subscribed': False
        #         }, 
        #             'post_author_data': {
        #                 'author': 876482061
        #             }, 
        #             'attachments': [], 
        #             'date': 1772086494, 
        #             'from_id': -236236878, 
        #             'id': 24, 
        #             'is_favorite': False, 
        #             'likes': {
        #                 'can_like': 1, 
        #                 'count': 0, 
        #                 'user_likes': 0, 
        #                 'can_publish': 1, 
        #                 'repost_disabled': False
        #             }, 
        #             'owner_id': -236236878, 
        #             'post_source': {
        #                 'type': 'api'
        #             }, 
        #             'post_type': 'post', 
        #             'reposts': {
        #                 'count': 0, 
        #                 'wall_count': 0, 
        #                 'mail_count': 0, 
        #                 'user_reposted': 0
        #             }, 
        #             'text': 'test post with kafka',
        #             'views': {
        #                 'count': 9
        #             }
        #         }
        #     ]
        # }
        print(f'try to get {count} posts of {group_id}')
        try:
            posts = self.vk.wall.get(domain=self.get_owner_id(group_id), count=count)
            print(posts)
        except Exception as e:
            print(e)
            return None, e
    
    async def get_user(self):
        print('try to get current user info')
        try:
            user = self.vk.users.get()
            print(user)
            await self.get_groups(user[0]['id'])
            return user
        except Exception as e:
            print(e)
            return None, e
        
    async def get_groups(self, user_id: int):
        print(f'try to fetch channels of user_id={user_id}')
        try:
            groups = self.vk.groups.get(user_id=user_id, extended=1)
            print(groups)
        except Exception as e:
            print(e)
            return None, e
