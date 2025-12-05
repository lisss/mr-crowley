import argparse
import sys
import time
from collections import deque
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup


class DualWriter:
    def __init__(self, file_path):
        self.file = open(file_path, "a")
        self.stdout = sys.stdout

    def write(self, text):
        self.file.write(text)
        self.file.flush()
        self.stdout.write(text)
        self.stdout.flush()

    def close(self):
        self.file.close()


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


class Fetcher:
    def __init__(self, user_agent="CrawleyBot/1.0"):
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def fetch(self, url):
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            final_url = response.url
            return True, response.text, response.status_code, final_url
        except requests.exceptions.RequestException:
            return False, None, None, url


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


class Extractor:
    def __init__(self, allowed_domain=None, deduplicator=None):
        self.allowed_domain = allowed_domain
        self.deduplicator = deduplicator or Deduplicator()

    def _is_allowed_domain(self, url):
        if self.allowed_domain is None:
            return True
        parsed = urlparse(url)
        return parsed.netloc == self.allowed_domain

    def extract(self, html, base_url):
        links = set()
        try:
            soup = BeautifulSoup(html, "html.parser")
            for anchor in soup.find_all("a", href=True):
                href = anchor["href"]
                absolute_url = urljoin(base_url, href)
                normalized = self.deduplicator.normalize(absolute_url)
                if self._is_allowed_domain(normalized):
                    links.add(normalized)
        except Exception as e:
            print(f"  Error parsing HTML: {e}", file=sys.stderr)
        return sorted(links)


class Crawley:
    def __init__(self, start_url, user_agent="CrawleyBot/1.0", allowed_domain=None):
        parsed = urlparse(start_url)
        if allowed_domain is None:
            allowed_domain = parsed.netloc

        self.deduplicator = Deduplicator()
        self.fetcher = Fetcher(user_agent)
        self.frontier = Frontier(start_url, user_agent, self.deduplicator)
        self.extractor = Extractor(allowed_domain, self.deduplicator)
        self.user_agent = user_agent
        self.start_url = start_url

    def crawl(self, output_file=None):
        if output_file:
            f = DualWriter(output_file)
        else:
            f = sys.stdout

        try:
            start_time = time.time()
            f.write(f"Starting crawl from: {self.start_url}\n")
            f.write(f"Domain: {self.frontier.base_netloc}\n\n")

            while self.frontier.has_next():
                url = self.frontier.get_next()

                if self.frontier.is_visited(url):
                    continue

                normalized_url = self.deduplicator.normalize(url)

                if not self.frontier.is_allowed(normalized_url):
                    f.write(f"Skipping (robots.txt): {normalized_url}\n")
                    self.frontier.mark_visited(normalized_url)
                    continue

                normalized_url = self.frontier.mark_visited(normalized_url)
                f.write(f"Visited: {normalized_url}\n")

                success, html, status_code, final_url = self.fetcher.fetch(normalized_url)

                if not success:
                    f.write(f"Failed to fetch: {normalized_url}\n")
                    if status_code:
                        f.write(f"  Status code: {status_code}\n")
                    self.frontier.mark_visited(normalized_url)
                    continue

                if final_url != normalized_url:
                    final_normalized = self.deduplicator.normalize(final_url)
                    if self.frontier.is_visited(final_normalized):
                        continue
                    normalized_url = self.frontier.mark_visited(final_normalized)
                    f.write(f"Visited: {normalized_url}\n")

                links = self.extractor.extract(html, normalized_url)
                added = self.frontier.add_urls(links)

            elapsed_time = time.time() - start_time
            f.write(
                f"\nCrawl complete. Visited {self.frontier.get_visited_count()} pages in {elapsed_time:.2f} seconds.\n"
            )
        finally:
            if output_file:
                f.close()


def main():
    parser = argparse.ArgumentParser(
        description="A simple web crawler that crawls pages on a single subdomain."
    )
    parser.add_argument("url", help="Starting URL to crawl (e.g., https://crawlme.monzo.com/)")
    parser.add_argument(
        "--user-agent",
        default="CrawleyBot/1.0",
        help="User agent string for HTTP requests (default: CrawleyBot/1.0)",
    )
    parser.add_argument(
        "--allowed-domain",
        default=None,
        help="Domain to allow crawling (default: same as starting URL domain)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file to write results to (default: stdout)",
    )

    args = parser.parse_args()

    parsed = urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        print(f"Error: Invalid URL: {args.url}", file=sys.stderr)
        sys.exit(1)

    crawler = Crawley(args.url, args.user_agent, args.allowed_domain)
    crawler.crawl(args.output)


if __name__ == "__main__":
    main()
