from collections import deque
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

from deduplicator import Deduplicator


class Frontier:
    def __init__(self, start_url, user_agent="CrawleyBot/1.0", deduplicator=None):
        self.deduplicator = deduplicator or Deduplicator()
        normalized_start = self.deduplicator.normalize(start_url)
        self.deduplicator.mark_seen(normalized_start)
        self.to_visit = deque([normalized_start])
        self.queued = {normalized_start}
        self.visited = set()
        self.robots_parser = None
        self.user_agent = user_agent
        parsed = urlparse(start_url)
        self.base_scheme = parsed.scheme
        self.base_netloc = parsed.netloc
        self._load_robots_txt()

    def _load_robots_txt(self):
        try:
            robots_url = f"{self.base_scheme}://{self.base_netloc}/robots.txt"
            session = requests.Session()
            session.headers.update({"User-Agent": self.user_agent})
            response = session.get(robots_url, timeout=5)
            if response.status_code == 200 and not response.text.strip().startswith("<?xml"):
                self.robots_parser = RobotFileParser()
                self.robots_parser.set_url(robots_url)
                self.robots_parser.read()
            else:
                self.robots_parser = None
        except Exception:
            self.robots_parser = None

    def has_next(self):
        return len(self.to_visit) > 0

    def get_next(self):
        if not self.has_next():
            return None
        url = self.to_visit.popleft()
        self.queued.discard(url)
        return url

    def is_visited(self, url):
        normalized = self.deduplicator.normalize(url)
        return normalized in self.visited

    def mark_visited(self, url):
        normalized = self.deduplicator.normalize(url)
        self.visited.add(normalized)
        self.deduplicator.mark_seen(normalized)
        return normalized

    def is_allowed(self, url):
        if self.robots_parser is None:
            return True
        return self.robots_parser.can_fetch(self.user_agent, url)

    def add_urls(self, urls):
        unique_urls = self.deduplicator.filter_unique(urls)
        added = []
        for url in unique_urls:
            if url not in self.visited and url not in self.queued:
                self.to_visit.append(url)
                self.queued.add(url)
                added.append(url)
        return added

    def get_visited_count(self):
        return len(self.visited)

