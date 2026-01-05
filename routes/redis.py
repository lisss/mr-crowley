import os
from flask import jsonify, redirect

from constants import (
    REDIS_KEY_VISITED, 
    REDIS_KEY_LEVEL, 
    REDIS_KEY_SEEN, 
    REDIS_KEY_QUEUED, 
    REDIS_KEY_QUEUE,
    ENV_REDIS_HOST, 
    ENV_REDIS_PORT
)


def get_redis_ui_url():
    redis_ui_url = os.getenv("REDIS_UI_URL")
    return jsonify({"url": redis_ui_url} if redis_ui_url else {})


def redis_ui():
    redis_ui_url = os.getenv("REDIS_UI_URL")
    if redis_ui_url:
        return redirect(redis_ui_url)
    else:
        return jsonify({"message": "Redis UI not configured"}), 404


def redis_health():
    try:
        from storage import Storage

        storage = Storage()
        storage.client.ping()

        visited_count = storage.client.scard(REDIS_KEY_VISITED)
        level_count = (
            storage.client.hlen(REDIS_KEY_LEVEL) if storage.client.exists(REDIS_KEY_LEVEL) else 0
        )

        return jsonify(
            {
                "status": "connected",
                "host": storage.redis_host,
                "port": storage.redis_port,
                "visited_count": visited_count,
                "level_count": level_count,
            }
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "error": str(e),
                    "host": os.getenv(ENV_REDIS_HOST, "not set"),
                    "port": os.getenv(ENV_REDIS_PORT, "not set"),
                }
            ),
            500,
        )


def get_metrics():
    try:
        from storage import Storage
        
        storage = Storage()
        storage.client.ping()
        
        visited_count = storage.client.scard(REDIS_KEY_VISITED)
        seen_count = storage.client.scard(REDIS_KEY_SEEN)
        queued_count = storage.client.scard(REDIS_KEY_QUEUED)
        queue_length = storage.client.llen(REDIS_KEY_QUEUE)
        
        # Generate a simple crawl_id based on visited count
        crawl_id = visited_count if visited_count > 0 else 1
        
        return jsonify({
            "crawl_id": crawl_id,
            "visited": visited_count,
            "seen": seen_count,
            "queued": queued_count,
            "queue_length": queue_length,
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "crawl_id": 0,
            "visited": 0,
            "seen": 0,
            "queued": 0,
            "queue_length": 0,
        }), 500


def get_queue():
    try:
        from storage import Storage
        
        storage = Storage()
        storage.client.ping()
        
        # Get all queue items (limited to first 100 for performance)
        queue_items = []
        queue_length = storage.client.llen(REDIS_KEY_QUEUE)
        
        if queue_length > 0:
            # Get first 100 items from queue
            queue_items = storage.client.lrange(REDIS_KEY_QUEUE, 0, 99)
        
        return jsonify({
            "queue": queue_items,
            "length": queue_length,
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "queue": [],
            "length": 0,
        }), 500

