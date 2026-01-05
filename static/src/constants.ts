export const DEFAULT_CRAWL_URL = "https://crawlme.monzo.com/";

export const METRICS_POLLING_INTERVAL = 5000;
export const LOGS_POLLING_INTERVAL = 5000;

export const API_ENDPOINTS = {
  START_CRAWL: "/api/crawl",
  STOP_CRAWL: "/api/stop-crawl", 
  LOGS: "/api/logs",
  METRICS: "/api/metrics",
  QUEUE: "/api/queue",
  VISITED_URLS: "/api/visited-urls",
  REDIS_UI_URL: "/api/redis-ui-url",
  REDIS_HEALTH: "/api/redis-health",
  CLEAR_LOGS: "/api/clear-logs"
} as const;

export const FORM_DEFAULTS = {
  URL_PLACEHOLDER: "https://crawlme.monzo.com/",
  MAX_LEVEL: 2,
  USE_STORAGE: false,
  CLEAR_STORAGE: false
} as const;
