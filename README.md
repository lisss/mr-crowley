# Crawley

![Crawley](crowley.jpg)

A simple web crawler that crawls all pages on a given subdomain.

## Features

- Crawls all pages on a single subdomain (e.g., `crawlme.monzo.com`)
- Does not follow external links to other domains or subdomains
- Prints each visited URL and the links found on that page
- Respects robots.txt
- Handles redirects and normalizes URLs
- Avoids infinite loops by tracking visited URLs

## Installation

Set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python crawler.py <starting_url>
```

### Example

```bash
python crawler.py https://crawlme.monzo.com/
```

The crawler will:
1. Start from the given URL
2. Visit each page on the same subdomain
3. Print each URL visited along with the links found on that page
4. Continue until all pages on the subdomain have been visited

### Options

- `--user-agent`: Specify a custom user agent string (default: `CrawleyBot/1.0`)
- `--allowed-domain`: Specify a domain to allow crawling (default: same as starting URL domain)

## Implementation Details

- Uses `requests` for HTTP requests
- Uses `beautifulsoup4` for HTML parsing
- Uses Python's standard library `urllib.parse` for URL handling
- Implements its own crawling logic (no frameworks like scrapy)
