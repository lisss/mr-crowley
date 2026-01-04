CLI USAGE:

python crawler.py <url> [options]

Arguments:
  url                    Starting URL to crawl (required)
  --user-agent           User agent (default: CrawleyBot/1.0)
  --allowed-domain       Domain to allow crawling (default: same as URL domain)
  --level                Maximum crawl depth (0=start URL only, 1=+direct links, etc.)
  --use-storage          Enable Redis persistent storage (default: in-memory)
  --clear-storage        Clear Redis storage before crawl (requires --use-storage)

Example:
python crawler.py https://crawlme.monzo.com/ --level 2 --use-storage --clear-storage

### Design approach

- UX: i started with cli (simple script) but ended up with web ui as it's more user-friendly (one doesn't need to run stuff in the inconvenient console, clicking buttons in web is always preferable for most people)
- intorduced max depth level for crawling - just for the sake of simplifying its testing (say, you just want to check that things work, you don't need to crawl the entire internet)
- using redis
  - once you crawl or repeat the crawling, you eventually end up with duplicating stuff you already seen
  - keeping that it the cache is a good idea for a fast access
  - also, we need peristence anyways, redis was a choice that combined both good caching solution and persistence storage
  - another option considered was to use some SQL DB (e.g. MySQL or Postgres), but for this task, I believe, redis is fine
  - it also adds an ability (via its IU) to check the raw data in the DB in case you're unsure
- CI/CD: i tried to apply some solution to automatically test & deploy the app, but for some reason nothing worked, so that I decided to postpone it for now



=================

BACKEND:
- crawler app itself (see diagram)
- redis as a storage (with its separate web ui interface to check its contents)

FRONTEND:
- entry-point UI to tune crawler and run/stop the process
- ability to check the results and see the persistent data in redis
