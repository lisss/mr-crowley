import os
from flask import jsonify, redirect

from constants import REDIS_KEY_VISITED, REDIS_KEY_LEVEL, ENV_REDIS_HOST, ENV_REDIS_PORT


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

