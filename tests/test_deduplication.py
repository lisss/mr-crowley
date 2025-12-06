import pytest

from deduplicator import Deduplicator
from frontier import Frontier


class TestDeduplication:
    def test_url_normalization_removes_trailing_slash(self):
        deduplicator = Deduplicator()
        assert deduplicator.normalize("https://crawlme.monzo.com/page/") == deduplicator.normalize("https://crawlme.monzo.com/page")

    def test_filter_unique_removes_duplicates(self):
        deduplicator = Deduplicator()
        urls = [
            "https://crawlme.monzo.com/page1",
            "https://crawlme.monzo.com/page1/",
            "https://crawlme.monzo.com/page2",
            "https://crawlme.monzo.com/page1",
        ]

        unique = deduplicator.filter_unique(urls)
        assert len(unique) == 2

    def test_frontier_prevents_adding_visited_urls(self):
        frontier = Frontier("https://crawlme.monzo.com/")
        url = "https://crawlme.monzo.com/page1"

        frontier.mark_visited(url)
        added = frontier.add_urls([url, url])
        assert len(added) == 0

    def test_frontier_deduplicates_before_adding(self):
        frontier = Frontier("https://crawlme.monzo.com/")
        urls = [
            "https://crawlme.monzo.com/page1",
            "https://crawlme.monzo.com/page1/",
            "https://crawlme.monzo.com/page2",
        ]

        added = frontier.add_urls(urls)
        assert len(added) == 2

        added_again = frontier.add_urls(urls)
        assert len(added_again) == 0

    def test_deduplication_persists_across_pages(self):
        deduplicator = Deduplicator()
        frontier = Frontier("https://crawlme.monzo.com/", deduplicator=deduplicator)

        urls_page1 = ["https://crawlme.monzo.com/page1", "https://crawlme.monzo.com/page2"]
        urls_page2 = ["https://crawlme.monzo.com/page1", "https://crawlme.monzo.com/page3"]

        added1 = frontier.add_urls(urls_page1)
        assert len(added1) == 2

        added2 = frontier.add_urls(urls_page2)
        assert len(added2) == 1
        assert "https://crawlme.monzo.com/page3" in added2
