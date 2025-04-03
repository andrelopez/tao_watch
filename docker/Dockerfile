FROM python:3.11-slim

WORKDIR /app/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (including OpenSSL development libraries and pkg-config)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       build-essential \
       libpq-dev \
       curl \
       pkg-config \
       libssl-dev \
       libffi-dev \
       python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Rust and Cargo
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y 
ENV PATH="/root/.cargo/bin:${PATH}"

# Set OpenSSL environment variables for aarch64 Debian systems
ENV OPENSSL_DIR="/usr"
ENV OPENSSL_LIB_DIR="/usr/lib/aarch64-linux-gnu"
ENV OPENSSL_INCLUDE_DIR="/usr/include/openssl"
ENV PKG_CONFIG_PATH="/usr/lib/aarch64-linux-gnu/pkgconfig"

# Install Python dependencies
COPY requirements/base.txt /app/requirements/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements/base.txt

# Copy project
COPY . /app/

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app
USER appuser

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]