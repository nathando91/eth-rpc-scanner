FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY ethereum_node_scanner.py .
COPY monitor_scan.py .

# Create directory for results
RUN mkdir -p /app/results

# Make scripts executable
RUN chmod +x ethereum_node_scanner.py monitor_scan.py

# Default command - run the scanner
CMD ["python3", "ethereum_node_scanner.py", "--asia-europe", "--timeout", "1", "--threads", "3000", "--output", "/app/results/ethereum_nodes.json"]
