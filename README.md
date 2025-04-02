# Tao Watch

A production-grade asynchronous API service for monitoring and interacting with the Bittensor blockchain.

## Project Overview

Tao Watch is a FastAPI-based service that:
- Provides authenticated endpoints to query Tao dividends from the Bittensor blockchain
- Caches blockchain query results in Redis
- Uses an asynchronous PostgreSQL database for historical data storage
- Leverages Celery for background task processing
- Optionally analyzes Twitter sentiment to make automated staking decisions

## Features

- **Blockchain Data Endpoint**: Query Tao dividends with optional caching
- **Authentication**: Secure API access using bearer tokens
- **Asynchronous Design**: Non-blocking I/O operations throughout
- **Background Processing**: Celery workers for handling long-running tasks
- **Containerization**: Docker and Docker Compose for easy deployment

## Project Structure

```
tao_watch/
├── app/                   # Main application package
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality (config, security)
│   ├── db/                # Database models and operations
│   ├── services/          # External services integration
│   └── tasks/             # Background tasks
├── tests/                 # Test suite
├── docker/                # Docker configuration
├── requirements/          # Dependency management
└── alembic/               # Database migrations
```

## Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/andrelopez/tao_watch.git
   cd tao_watch
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements/dev.txt
   ```

4. Set up environment variables (copy from example):
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Running with Docker

1. Build and start all services:
   ```bash
   docker compose up --build
   ```

2. Or run in detached mode:
   ```bash
   docker compose up -d
   ```

3. View logs:
   ```bash
   docker compose logs -f
   ```

4. Access the API documentation:
   ```
   http://localhost:8000/docs
   ```

5. Stop services:
   ```bash
   docker compose down
   ```

6. Clean up all containers, including orphaned ones:
   ```bash
   docker compose down --remove-orphans
   ```

## Testing

### Running Tests with Docker (Recommended)

This is the most reliable way to run tests as it ensures a consistent environment:

```bash
# Build and run tests
docker compose build api && docker compose run api pytest
```

For verbose output:

```bash
docker compose run api pytest -sv
```

To run specific tests:

```bash
docker compose run api pytest tests/api/test_health.py -v
```

### Running Tests Locally

If you prefer to run tests outside of Docker (requires Redis and PostgreSQL running locally):

```bash
# Activate virtual environment first
pytest
```

For verbose output:

```bash
pytest -sv
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

[MIT License](LICENSE) 