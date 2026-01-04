import pytest

from deduplicator import Deduplicator
from frontier import Frontier


class TestDeduplication:
    def test_url_normalization_works(self):
        deduplicator = Deduplicator()
        assert deduplicator.normalize("https://crawlme.monzo.com/page/") == deduplicator.normalize(
            "https://crawlme.monzo.com/page"
        )

    def test_duplicate_filtering_works(self):
        deduplicator = Deduplicator()
        urls = [
            "https://crawlme.monzo.com/page1",
            "https://crawlme.monzo.com/page1/",
            "https://crawlme.monzo.com/page2",
            "https://crawlme.monzo.com/page1",
        ]

        unique = deduplicator.filter_unique(urls)
        assert len(unique) == 2

    def test_frontier_prevents_re_adding_visited_urls(self):
        frontier = Frontier("https://crawlme.monzo.com/")
        urls = [
            "https://crawlme.monzo.com/page1",
            "https://crawlme.monzo.com/page1/",
            "https://crawlme.monzo.com/page2",
        ]

        added = frontier.add_urls(urls)
        assert len(added) == 2

        frontier.mark_visited("https://crawlme.monzo.com/page1")
        added_again = frontier.add_urls(urls)
        assert len(added_again) == 0
