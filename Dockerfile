FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY package.json ./
COPY tsconfig.json ./
COPY scripts ./scripts
COPY static/src ./static/src
RUN npm install && npm run build

COPY *.py ./
COPY static/css ./static/css
COPY static/dist ./static/dist

EXPOSE 5000

ENTRYPOINT []
CMD ["python", "web.py"]

