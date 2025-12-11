# System Overview

```
Browser → Flask API → Crawler subprocess → Redis
```

UI calls Flask endpoints. Flask spawns crawler. Crawler writes to Redis.
