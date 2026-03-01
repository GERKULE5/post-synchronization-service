class KafkaBase:
    def __init__(self, url: str):
        self.url = url
        self._client = None
    
    async def stop(self):
        if self._client:
            await self._client.stop()
            