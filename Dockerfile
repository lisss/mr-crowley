FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY package.json package-lock.json ./
COPY tsconfig.json ./
COPY static/src ./static/src
COPY static/css ./static/css
RUN npm install && npm run build:less && npx tsc

COPY scripts/bundle.js /tmp/create-bundle.js
RUN node /tmp/create-bundle.js && \
    rm /tmp/create-bundle.js && \
    test -f static/dist/bundle.js || (echo "ERROR: bundle.js not created!" && exit 1) && \
    echo "Bundle created at: $(pwd)/static/dist/bundle.js" && \
    ls -lh static/dist/bundle.js

COPY *.py ./
COPY routes ./routes
COPY crawler ./crawler
COPY frontier ./frontier
COPY deduplicator ./deduplicator
COPY extractor ./extractor
COPY fetcher.py ./
COPY storage.py ./
COPY static/index.html ./static/index.html

RUN echo "=== Final verification ===" && \
    find static/dist -name "bundle.js" -type f && \
    test -f static/dist/bundle.js && echo "✓ bundle.js EXISTS at $(pwd)/static/dist/bundle.js" || (echo "✗ bundle.js MISSING!" && find static -name "*.js" -type f | head -5 && exit 1)

EXPOSE 5000

ENTRYPOINT []
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120 --access-logfile - --error-logfile - web:app"]
