from abc import ABC, abstractmethod
from typing import Optional


class BasePublisher(ABC):
    def __init__(self, token: str):
        self.token = token

    @abstractmethod
    async def initialize(self) -> bool:
        pass

    @abstractmethod
    async def upload_post(self, group_id: int, message: str):
        pass

    @abstractmethod
    async def edit_post(self, group_id: int, post_id: int, message: str):
        pass

    @abstractmethod
    async def delete_post(self, group_id: int, post_id: int):
        pass

    @abstractmethod
    async def restore_post(self, group_id: int, post_id: int):
        pass

    @abstractmethod
    async def pin_post(self, group_id: int, post_id: int):
        pass

    @abstractmethod
    async def get_posts(self, group_id: int, post_id: int):
        pass

    @abstractmethod
    async def get_user(self):
        pass

    @abstractmethod
    async def get_groups(self, group_id: int):
        pass
