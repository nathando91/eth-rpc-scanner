#!/bin/bash

echo "🐳 Ethereum Node Scanner - Docker Setup"
echo "========================================"

# Create directories
mkdir -p results logs

# Build and run with docker-compose
echo "Building Docker images..."
docker-compose build

echo "Starting Ethereum scanner in background..."
docker-compose up -d

echo ""
echo "✅ Services started:"
echo "  - ethereum-scanner: Main scanning service"
echo "  - monitor: Progress monitoring service"
echo ""
echo "📊 Commands:"
echo "  docker-compose logs -f ethereum-scanner    # View scanner logs"
echo "  docker-compose logs -f monitor             # View monitor logs"
echo "  docker-compose ps                          # Check status"
echo "  docker-compose stop                        # Stop services"
echo "  docker-compose down                        # Stop and remove"
echo ""
echo "📁 Results will be saved to: ./results/"
echo "📋 Logs will be saved to: ./logs/"
echo ""
echo "🔍 Monitor progress:"
echo "  docker-compose exec monitor python3 monitor_scan.py"
