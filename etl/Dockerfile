FROM python:3.11-slim

WORKDIR /etl

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY data/ ./data/

# Create logs directory
RUN mkdir -p /etl/logs

ENV PYTHONPATH=/etl

CMD ["python", "src/main.py"]
