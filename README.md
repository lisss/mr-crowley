# Crawley

Meet Mr. Crowley - a web crawler :)

![Crawley](./public/images/crowley.jpg)

## What it does consist of

### Front-end
#### CLI
You can use CLI if you wish, it's as simple as this: `python crawler.py <url> [options]` TODO: link

#### Web UI
A convenient UI to run/stop the crawler. Baked with React and TypeScript. Shows real-time progress, logs. You can see how many pages it found and browse the results (both at the curren UI page or navigating to the Redis web UI console)

### Backend
Python & Flask. Divided into modules:
- **Crawler**: The heart of the system, broken into modular components:
  - **Frontier**: The traffic controller - manages what to crawl next and makes sure we stay on the right domain
  - **Fetcher**: Actually downloads the web pages (and deals with all the ways that can go wrong)
  - **Extractor**: Pulls links out of HTML and filters them  
  - **Deduplicator**: Makes sure we don't crawl the same page twice
- **Storage**: Redis persistence with in-memory fallback - saves stuff either to Redis or just in memory, depending on what you want



🐧 The diagram can bee seen here:
![System Architecture](./public/images/sd-diagram.png)


### Deployment
Docker compose with three containers - main app, Redis database, and Redis admin UI

#### Testing
pytest on the backend (no FE tests so far...):
```bash
pytest tests/ -v
```

### Design approach TODO - add icon and refine
- Stays on one domain like a good little bot (but you can change which domain)
- Respects robots.txt because I'm not a monster
- Won't crawl the same page twice (even if the URLs look slightly different)
- Handles errors gracefully instead of just exploding
- UX: i started with cli (simple script) but ended up with web ui as it's more user-friendly (one doesn't need to run stuff in the inconvenient console, clicking buttons in web is always preferable for most people)
- intorduced max depth level for crawling - just for the sake of simplifying its testing (say, you just want to check that things work, you don't need to crawl the entire internet)
- using redis
  - once you crawl or repeat the crawling, you eventually end up with duplicating stuff you already seen
  - keeping that it the cache is a good idea for a fast access
  - also, we need peristence anyways, redis was a choice that combined both good caching solution and persistence storage
  - another option considered was to use some SQL DB (e.g. MySQL or Postgres), but for this task, I believe, redis is fine
  - it also adds an ability (via its IU) to check the raw data in the DB in case you're unsure
- CI/CD: i tried to apply some solution to automatically test & deploy the app, but for some reason nothing worked, so that I decided to postpone it for now

## Getting Started

### Development

If you want to run locally (did not properly tested, sorry, I believe it would work but can't guarantee)
#### Back-end
```bash
pip install -r requirements.txt
npm install
npm run build
python web.py
```

### Frontend
```bash
npm run watch
npm run watch:less
```

### Using Docker
```bash
docker-compose up -d
```

Open `http://localhost:5002` and you're good to go.

## How to Use It

### Web UI
1. Put in a URL you want to crawl (like `https://crawlme.monzo.com/`)
2. Tweak the settings if you want:
   - **User Agent**: What the crawler identifies itself as (some sites care about this)
   - **Allowed Domain**: Keep it on one domain or let it wander (probably keep it restricted)  
   - **Crawl Depth**: How many "clicks" deep to go (0 = just the start page, 1 = start page + links from it, etc.)
   - **Redis Storage**: Check this if you want your results to stick around after you close the browser
3. Hit "Start Crawl" and watch it do its thing

### The Old-School Way (Command Line)]
`python crawler.py <url> [options]`

```
Arguments:
  url                    Starting URL to crawl (required)
  --user-agent           User agent (default: CrawleyBot/1.0)
  --allowed-domain       Domain to allow crawling (default: same as URL domain)
  --level                Maximum crawl depth (0=start URL only, 1=+direct links, etc.)
  --use-storage          Enable Redis persistent storage (default: in-memory)
  --clear-storage        Clear Redis storage before crawl (requires --use-storage)
```

Example:
`python crawler.py https://crawlme.monzo.com/ --level 2 --use-storage --clear-storage`

## Configuration

You can tweak these environment variables if needed:
- `REDIS_HOST`: Where to find Redis (defaults to localhost)
- `REDIS_PASSWORD`: Redis password if you have one set up
- `PORT`: What port the web server runs on (defaults to 5000)
- `FLASK_DEBUG`: Set to 1 if you want verbose debug output