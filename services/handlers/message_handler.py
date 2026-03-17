from typing import Dict
from services.publishers.factory import PublisherFactory


class MessageHandler:
    def __init__(self, producer=None):
        self.producer = producer

    async def handle(self, message: Dict, headers: Dict = {}):
        print(message)
        print('start handling')

        event_type = message.get("event_type")

        if not event_type:
            print("No event_type in message, skipping")
            return

        handler = self._get_handler(event_type)

        if handler is None:
            print(f"Unknown event_type: {event_type}")
            return

        await handler(message, headers)

    def _get_handler(self, event_type: str):
        return {
            'UPLOAD':  self._handle_upload,
            'EDIT':    self._handle_edit,
            'DELETE':  self._handle_delete,
            'RESTORE': self._handle_restore,
            'PIN':     self._handle_pin,
            'SYNC':    self._handle_sync,
            'FETCH':   self._handle_fetch,
        }.get(event_type)

    def _requires_vk(self, message: Dict) -> tuple[bool, list]:
        platform     = message.get("platform", [])
        vk_group_ids = message.get("group_ids", [])

        if 'vk' not in platform:
            print(f"Platform 'vk' not in platform_type: {platform}")
            return False, []

        if not vk_group_ids:
            print("No vk_group_ids provided")
            return False, []

        return True, vk_group_ids

    async def _get_publisher(self, message: Dict):
        platform = message.get("platform")
        token    = message.get("token")

        if platform != 'vk' or not token or not platform:
            print("Missing platform or token")
            return None

        publisher = PublisherFactory.create('vk', token)
        await publisher.initialize()
        return publisher

    async def _handle_upload(self, message: Dict, headers: Dict):
        ok, vk_group_ids = self._requires_vk(message)
        if not ok:
            return

        publisher = await self._get_publisher(message)
        if not publisher:
            return

        news_id = message.get('news_id')
        institution_id = message.get('institution_id')
        is_pinned = message.get("isPinned")
        
        text = f"{message.get('title')}\n{message.get('content')}"

        try:
            for group_id in vk_group_ids:
                post = await publisher.upload_post(group_id, text)
                print(post)

                if is_pinned is True:
                    await publisher.pin_post(group_id, post.get('post_id'))

                await self.producer.send('posts.reply', {
                    'news_id': news_id,
                    'institution_id': institution_id,
                    'group_id': group_id,
                    'post_id': post['post_id'],
                    'status': 'UPLOADED',
                    'platform': 'vk',
                })
        finally:
            await publisher.close()

    async def _handle_edit(self, message: Dict, headers: Dict):
        ok, vk_group_ids = self._requires_vk(message)
        if not ok:
            return

        publisher = await self._get_publisher(message)
        if not publisher:
            return

        id = message.get('id')
        executor_id = message.get('executorId')
        post_id = message.get('post_id')
        text = f"{message.get('title')}\n{message.get('content')}"

        try:
            for group_id in vk_group_ids:
                post = await publisher.edit_post(group_id, post_id, text)
                if post:
                    await self.producer.send('posts.reply', {
                        'executor_id': executor_id,
                        'news_id':     id,
                        'post_id':     post['post_id'],
                        'status':      'EDITED',
                    })
        finally:
            await publisher.close()

    async def _handle_delete(self, message: Dict, headers: Dict):
        ok, vk_group_ids = self._requires_vk(message)
        if not ok:
            return

        publisher = await self._get_publisher(message)
        if not publisher:
            return

        id = message.get('id')
        executor_id = message.get('executorId')
        post_id = message.get('post_id')

        try:
            for group_id in vk_group_ids:
                post = await publisher.delete_post(group_id, post_id)
                if post:
                    await self.producer.send('posts.reply', {
                        'executor_id': executor_id,
                        'news_id':     id,
                        'status':      'deleted',
                    })
        finally:
            await publisher.close()

    async def _handle_restore(self, message: Dict, headers: Dict):
        ok, vk_group_ids = self._requires_vk(message)
        if not ok:
            return

        publisher = await self._get_publisher(message)
        if not publisher:
            return

        id = message.get('id')
        executor_id = message.get('executorId')
        post_id = message.get('post_id')

        try:
            for group_id in vk_group_ids:
                post = await publisher.restore_post(group_id, post_id)
                if post:
                    await self.producer.send('posts.reply', {
                        'executor_id': executor_id,
                        'news_id':     id,
                        'status':      'RESTORED',
                    })
        finally:
            await publisher.close()

    async def _handle_pin(self, message: Dict, headers: Dict):
        ok, vk_group_ids = self._requires_vk(message)
        if not ok:
            return

        publisher = await self._get_publisher(message)
        if not publisher:
            return

        post_id = message.get('post_id')

        try:
            for group_id in vk_group_ids:
                await publisher.pin_post(group_id, post_id)
        finally:
            await publisher.close()

    async def _handle_sync(self, message: Dict, headers: Dict):
        print('SYNC is handled')

    async def _handle_fetch(self, message: Dict, headers: Dict):
        correlation_id = headers.get('kafka_correlationId')
        reply_topic = headers.get('kafka_replyTopic', 'posts.reply')
        platform = message.get("platform")
        token = message.get("token")

        if not platform or not token:
            print("FETCH: missing platform or token")
            return

        publisher = PublisherFactory.create(platform, token)
        await publisher.initialize()

        try:
            user = await publisher.get_user()
            groups = await publisher.get_groups(user[0]['id'])

            await self.producer.send(
                reply_topic,
                {'channels': groups.get('items', []) if groups else []},
                headers={'kafka_correlationId': correlation_id},
            )
            print('FETCH is handled')
        finally:
            await publisher.close()