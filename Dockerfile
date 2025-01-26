FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y \
    gcc \
    librdkafka-dev \
    python3-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt
COPY app/ ./app
COPY tests/ ./tests
EXPOSE 3000
CMD ["/bin/sh", "-c", "if [ \"$ENABLE_KAFKA\" = \"1\" ]; then gunicorn -w 4 -b 0.0.0.0:3000 app.app:app; else python app/app.py; fi"]
