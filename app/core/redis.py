import redis
import os
from app.core.exceptions import AppException

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class RedisClient:
    _client = None

    @classmethod
    def get(cls):
        if cls._client:
            return cls._client

        try:
            cls._client = redis.Redis.from_url(
                REDIS_URL,
                decode_responses=True
            )

            # test connection
            cls._client.ping()
    
            return cls._client

        except Exception as e:
            print("⚠️ Redis not available:", e)
            cls._client = None
            return None