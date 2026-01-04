import os
import sys
from urllib.parse import urlparse

from deduplicator.deduplicator import Deduplicator
from extractor.extractor import Extractor
from fetcher import Fetcher
from frontier.frontier import Frontier
from storage import Storage
from constants import (
    REDIS_KEY_VISITED,
    REDIS_KEY_QUEUED,
    REDIS_KEY_QUEUE,
    REDIS_KEY_LEVEL,
    REDIS_KEY_SEEN,
)


def init_crawler(start_url, user_agent, allowed_domain, use_storage, max_level, clear_storage):
    parsed = urlparse(start_url)
    if allowed_domain is None:
        allowed_domain = parsed.netloc

    storage = None
    if use_storage:
        try:
            storage = Storage()
            storage.client.ping()
            if clear_storage:
                keys = [
                    REDIS_KEY_VISITED,
                    REDIS_KEY_QUEUED,
                    REDIS_KEY_QUEUE,
                    REDIS_KEY_LEVEL,
                    REDIS_KEY_SEEN,
                ]
                for key in keys:
                    storage.client.delete(key)
                print("Cleared Redis storage.", file=sys.stdout)
            else:
                # Check if we need to explore deeper
                prev_max_level = 0
                if storage.client.exists(REDIS_KEY_LEVEL):
                    all_levels = storage.client.hgetall(REDIS_KEY_LEVEL)
                    if all_levels:
                        prev_max_level = max(int(level) for level in all_levels.values())

                print(
                    f"Previous max level: {prev_max_level}, new max level: {max_level}",
                    file=sys.stdout,
                )

                if max_level is not None and max_level > prev_max_level:
                    # Need to go deeper - add boundary URLs back to queue for re-examination
                    if all_levels:
                        boundary_urls = [
                            url
                            for url, level_str in all_levels.items()
                            if int(level_str) == prev_max_level
                        ]
                        if boundary_urls:
                            # Clear queue and add boundary URLs for deeper exploration
                            storage.client.delete(REDIS_KEY_QUEUED)
                            storage.client.delete(REDIS_KEY_QUEUE)

                            # Add boundary URLs back to queue (but keep them in visited)
                            for url in boundary_urls:
                                storage.add_to_list(REDIS_KEY_QUEUE, url)
                                storage.add_to_set(REDIS_KEY_QUEUED, url)

                            print(
                                f"Re-queued {len(boundary_urls)} boundary URLs for deeper exploration.",
                                file=sys.stdout,
                            )

                # Always ensure start URL is in queue if queue is empty
                if storage.get_list_length(REDIS_KEY_QUEUE) == 0:
                    if not storage.is_in_set(REDIS_KEY_QUEUED, normalized_start):
                        storage.add_to_list(REDIS_KEY_QUEUE, normalized_start)
                        storage.add_to_set(REDIS_KEY_QUEUED, normalized_start)
        except Exception as e:
            print(
                f"Warning: Could not connect to Redis: {e}. Using in-memory storage.",
                file=sys.stderr,
            )
            storage = None

    deduplicator = Deduplicator(storage)
    fetcher = Fetcher(user_agent)
    frontier = Frontier(start_url, user_agent, deduplicator, storage, max_level)
    extractor = Extractor(allowed_domain, deduplicator)

    return {
        "storage": storage,
        "deduplicator": deduplicator,
        "fetcher": fetcher,
        "frontier": frontier,
        "extractor": extractor,
        "user_agent": user_agent,
        "start_url": start_url,
        "max_level": max_level,
    }
