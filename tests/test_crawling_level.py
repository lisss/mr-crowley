import pytest

from frontier import Frontier
from constants import DEFAULT_CRAWL_URL


class TestLevelBasedCrawling:
    def test_level_0_only_processes_start_url(self):
        frontier = Frontier(DEFAULT_CRAWL_URL, max_level=0)
        
        url, level = frontier.get_next()
        assert url == DEFAULT_CRAWL_URL
        assert level == 0
        
        assert not frontier.has_next()

    def test_level_limits_prevent_infinite_crawling(self):
        frontier = Frontier(DEFAULT_CRAWL_URL, max_level=1)
        
        url, level = frontier.get_next()
        assert level == 0
        
        links = [f"{DEFAULT_CRAWL_URL}page1", f"{DEFAULT_CRAWL_URL}page2"]
        added = frontier.add_urls(links, current_level=0)
        assert len(added) == 2
        
        url1, level1 = frontier.get_next()
        assert level1 == 1
        
        added_beyond = frontier.add_urls(links, current_level=1)
        assert len(added_beyond) == 0
