# Crawley

![Crawley](crowley.jpg)

A simple web crawler with a web UI.

## Quick Start

Start the web interface:
```bash
python web.py
```

Then open http://localhost:5000

## CLI Usage

```bash
python crawler.py https://crawlme.monzo.com/ --level 5 --use-storage
```

Options:
- `--user-agent`: Custom user agent
- `--allowed-domain`: Domain to crawl (default: same as start URL)
- `--use-storage`: Enable Redis storage
- `--level`: Max crawl depth
- `--clear-storage`: Clear Redis before starting

## Docker

```bash
docker-compose up -d
```

Web UI: http://localhost:5000

## Deployment

See `DEPLOY.md` for deployment instructions.
