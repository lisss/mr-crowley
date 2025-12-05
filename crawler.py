import argparse
import sys
from urllib.parse import urlparse

from crawley import Crawley


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
