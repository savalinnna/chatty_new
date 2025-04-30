import redis.asyncio as redis
from app.core.config import settings
import json
from typing import List, Optional

redis_client = redis.from_url(settings.redis_url)

async def get_cached_feed(user_id: int) -> Optional[List[dict]]:
    """Retrieve cached feed for a user."""
    cache_key = f"feed:{user_id}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    return None

async def set_cached_feed(user_id: int, posts: List[dict]) -> None:
    """Cache feed for a user."""
    cache_key = f"feed:{user_id}"
    await redis_client.setex(cache_key, 3600, json.dumps(posts))

async def invalidate_feeds_of_followers(follower_ids: List[int]) -> None:
    """Invalidate cached feeds for a list of followers."""
    for follower_id in follower_ids:
        cache_key = f"feed:{follower_id}"
        await redis_client.delete(cache_key)