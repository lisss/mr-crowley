import pytest

from deduplicator import Deduplicator
from frontier import Frontier
from constants import DEFAULT_CRAWL_URL


class TestDeduplication:
    def test_url_normalization_works(self):
        deduplicator = Deduplicator()
        assert deduplicator.normalize(f"{DEFAULT_CRAWL_URL}page/") == deduplicator.normalize(
            f"{DEFAULT_CRAWL_URL}page"
        )

    def test_duplicate_filtering_works(self):
        deduplicator = Deduplicator()
        urls = [
            f"{DEFAULT_CRAWL_URL}page1",
            f"{DEFAULT_CRAWL_URL}page1/",
            f"{DEFAULT_CRAWL_URL}page2",
            f"{DEFAULT_CRAWL_URL}page1",
        ]

        unique = deduplicator.filter_unique(urls)
        assert len(unique) == 2

    def test_frontier_prevents_re_adding_visited_urls(self):
        frontier = Frontier(DEFAULT_CRAWL_URL)
        urls = [
            f"{DEFAULT_CRAWL_URL}page1",
            f"{DEFAULT_CRAWL_URL}page1/",
            f"{DEFAULT_CRAWL_URL}page2",
        ]

        added = frontier.add_urls(urls)
        assert len(added) == 2

        frontier.mark_visited(f"{DEFAULT_CRAWL_URL}page1")
        added_again = frontier.add_urls(urls)
        assert len(added_again) == 0
