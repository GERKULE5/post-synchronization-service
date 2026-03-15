from services.publishers.base import BasePublisher
from services.publishers.vk.publish import VkPublisher


class PublisherFactory:
    @staticmethod
    def create(platform: str, token: str) -> BasePublisher:
        if platform == 'vk':
            return VkPublisher(token)
        # elif platform == 'telegram':
        #     return TelegramPublisher(token)
        raise ValueError(f'Unknown platform: {platform}')
