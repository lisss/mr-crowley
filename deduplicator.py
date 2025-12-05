from urllib.parse import urlparse


class Deduplicator:
    def __init__(self):
        self.seen = set()

    def normalize(self, url):
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        if normalized.endswith("/") and len(parsed.path) > 1:
            normalized = normalized[:-1]
        return normalized

    def is_seen(self, url):
        normalized = self.normalize(url)
        return normalized in self.seen

    def mark_seen(self, url):
        normalized = self.normalize(url)
        self.seen.add(normalized)
        return normalized

    def filter_unique(self, urls):
        seen_in_list = set()
        unique = []
        for url in urls:
            normalized = self.normalize(url)
            if normalized not in self.seen and normalized not in seen_in_list:
                seen_in_list.add(normalized)
                unique.append(normalized)
                self.seen.add(normalized)
        return unique

    def get_seen_count(self):
        return len(self.seen)

