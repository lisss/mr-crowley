"""
Constants used throughout the Crowley web crawler application.
"""

# Default URLs
DEFAULT_CRAWL_URL = "https://crawlme.monzo.com/"

# Server Configuration
DEFAULT_WEB_PORT = 5000
DEFAULT_REDIS_PORT = 6379
DOCKER_WEB_PORT = 5002

# Redis Keys
REDIS_KEY_VISITED = "crawley:visited"
REDIS_KEY_QUEUED = "crawley:queued"
REDIS_KEY_QUEUE = "crawley:queue"
REDIS_KEY_LEVEL = "crawley:level"
REDIS_KEY_SEEN = "crawley:seen"

# Environment Variables
ENV_REDIS_HOST = "REDIS_HOST"
ENV_REDIS_PASSWORD = "REDIS_PASSWORD"
ENV_REDIS_PORT = "REDIS_PORT"
ENV_PORT = "PORT"

# Polling Intervals (in milliseconds)
METRICS_POLLING_INTERVAL = 5000
LOGS_POLLING_INTERVAL = 5000

# Default Values
DEFAULT_REDIS_HOST = "localhost"
DEFAULT_MAX_WORKERS = 2
DEFAULT_MAX_THREADS = 2
DEFAULT_TIMEOUT = 120

# Cache Configuration
CACHE_SIZE_LIMIT = 10000  # Assuming this from storage.py implementation

# Web Server Configuration
WEB_SERVER_HOST = "0.0.0.0"
DEBUG_MODE = False
