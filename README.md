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
- Persistent storage using Redis (with in-memory fallback)
- Dockerized services for easy deployment

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

### Quick Testing with Depth Limit

To test the crawler quickly without running a full crawl, use the `--level` option:

```bash
# Only crawl the start URL
python crawler.py https://crawlme.monzo.com/ --level 0

# Crawl start URL + links un to level N
python crawler.py https://crawlme.monzo.com/ --level N
```

### Options

- `--user-agent`: Specify a custom user agent string (default: `CrawleyBot/1.0`)
- `--allowed-domain`: Specify a domain to allow crawling (default: same as starting URL domain)
- `--output`: Output file to write results to (default: stdout)
- `--use-storage`: Enable Redis storage (default: in-memory for speed)
- `--level`: Maximum crawl depth level (0 = start URL only, 1 = start URL + direct links, etc.). Useful for quick testing without running a full crawl.

## Docker Usage

The project includes Docker support with separate services for Redis and the crawler.

### Prerequisites

- Docker and Docker Compose installed

### Running with Docker Compose

```bash
# Build/rebuild the Docker image (required after code changes)
docker-compose build

# Start Redis and crawler services (container will wait for commands)
# If containers are already running, restart them to use the new image
docker-compose up -d --force-recreate

# Run the crawler manually
docker exec -it crawley-crawler python crawler.py https://crawlme.monzo.com/ --output results.txt --use-storage

# Or with custom options (e.g., limit crawl depth to 2 levels for quick testing)
docker exec -it crawley-crawler python crawler.py https://crawlme.monzo.com/ --output results.txt --use-storage --level 2

# Or with multiple custom options
docker exec -it crawley-crawler python crawler.py https://crawlme.monzo.com/ --output results.txt --use-storage --user-agent "MyBot/1.0" --level 3
```

### Running Individual Services

```bash
# Build the crawler image
docker build -t crawley .

# Run Redis container
docker run -d --name crawley-redis -p 6379:6379 -v redis-data:/data redis:7-alpine redis-server --appendonly yes

# Run crawler container (keeps running, waiting for commands)
docker run -d --name crawley-crawler --link crawley-redis:redis -e REDIS_HOST=redis -e REDIS_PORT=6379 -v $(pwd)/results.txt:/app/results.txt crawley

# Execute crawler command
docker exec -it crawley-crawler python crawler.py https://crawlme.monzo.com/ --output results.txt --use-storage

# Or with depth limit for quick testing
docker exec -it crawley-crawler python crawler.py https://crawlme.monzo.com/ --output results.txt --use-storage --level 2
```

## Storage

The crawler uses Redis for persistent storage by default:
- **Visited URLs**: Stored in Redis set `crawley:visited`
- **Queued URLs**: Stored in Redis set `crawley:queued`
- **URL Queue**: Stored in Redis list `crawley:queue`
- **Seen URLs**: Stored in Redis set `crawley:seen`

If Redis is unavailable, the crawler automatically falls back to in-memory storage.

### Redis Configuration

Set environment variables to configure Redis connection:
- `REDIS_HOST`: Redis host (default: `localhost`)
- `REDIS_PORT`: Redis port (default: `6379`)

### Accessing Redis Data

To inspect what's stored in Redis:

```bash
# Access Redis CLI
docker exec -it crawley-redis redis-cli

# Commands:
docker exec -it crawley-redis redis-cli KEYS "*"
docker exec -it crawley-redis redis-cli SCARD crawley:visited     # Visited URLs
docker exec -it crawley-redis redis-cli SCARD crawley:queued      # Queued URLs
docker exec -it crawley-redis redis-cli LLEN crawley:queue        # Queue length
docker exec -it crawley-redis redis-cli SCARD crawley:seen        # Seen URLs
docker exec -it crawley-redis redis-cli SMEMBERS crawley:visited | head -10
docker exec -it crawley-redis redis-cli LRANGE crawley:queue 0 9
docker exec -it crawley-redis redis-cli DEL crawley:visited crawley:queued crawley:queue crawley:seen
```

## Implementation Details

- Uses `requests` for HTTP requests
- Uses `beautifulsoup4` for HTML parsing
- Uses Python's standard library `urllib.parse` for URL handling
- Implements its own crawling logic (no frameworks like scrapy)
