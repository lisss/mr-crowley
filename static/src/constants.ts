/**
 * Constants used throughout the Crowley web crawler frontend application.
 */

// Default URLs
export const DEFAULT_CRAWL_URL = "https://crawlme.monzo.com/";

// Polling Intervals (in milliseconds)
export const METRICS_POLLING_INTERVAL = 5000;
export const LOGS_POLLING_INTERVAL = 5000;

// API Endpoints
export const API_ENDPOINTS = {
  START_CRAWL: "/api/crawl/start",
  STOP_CRAWL: "/api/crawl/stop", 
  LOGS: "/api/crawl/logs",
  METRICS: "/api/metrics",
  QUEUE: "/api/queue",
  VISITED_URLS: "/api/visited-urls",
  REDIS_UI_URL: "/api/redis-ui-url",
  REDIS_HEALTH: "/api/redis-health",
  CLEAR_LOGS: "/api/crawl/clear-logs"
} as const;

// Form Configuration
export const FORM_DEFAULTS = {
  URL_PLACEHOLDER: "https://crawlme.monzo.com/",
  MAX_LEVEL: 2,
  USE_STORAGE: false,
  CLEAR_STORAGE: false
} as const;
