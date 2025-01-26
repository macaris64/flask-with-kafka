# Flask With Kafka

### Setup

#### For local development

1. Clone the repository
2. Create a virtual environment
3. Install the dependencies
4. Run the server

```bash
git clone <>
cd flask-with-kafka
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn -w 4 -b 127.0.0.1:3000 app.app:app
ENABLE_KAFKA=1 FLASK_DEBUG=1 gunicorn -w 4 -b 127.0.0.1:3000 app.app:app
```

#### For local development with Docker
1. Clone the repository
2. Build the docker image
3. Run the docker container

```bash
git clone <>
cd flask-with-kafka
docker-compose up --build
```

#### Run tests in Local
```bash
pytest
```

#### Run tests in Local With Coverage
```bash
pytest --cov=app --cov-report=term-missing
open htmlcov/index.html
```

#### Run tests in Docker
```bash
docker-compose up tests
docker-compose up tests-with-coverage
docker cp <container_id>:/app/htmlcov ./htmlcov
open htmlcov/index.html
```
