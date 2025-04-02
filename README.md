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

- Python 3.9+
- Docker and Docker Compose
- Git

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tao_watch.git
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
   docker-compose up --build
   ```

2. Access the API documentation:
   ```
   http://localhost:8000/docs
   ```

## Testing

Run the test suite with:

```bash
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