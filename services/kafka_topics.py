from typing import Dict, Any

class KafkaTopicConfig:
    """Конфигурация топика Kafka"""
    name: str
    num_partitions: int = 3
    replication_factor: int = 1
    config: Dict[str, Any] = None

TOPIC_CONFIGS = {
    'posts': KafkaTopicConfig(
        name = 'posts',
        num_partitions = 3,
        replication_factor = 1,
        config = {
            'retention.ms': '60000'
        }
    )
}