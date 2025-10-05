# 🐳 Ethereum Node Scanner - Docker Setup

## Quick Start

### 1. Chạy với Docker Compose (Khuyến nghị)
```bash
# Chạy script tự động
./run_docker.sh

# Hoặc chạy thủ công
docker-compose up -d
```

### 2. Chạy với Docker trực tiếp
```bash
# Build image
docker build -t ethereum-scanner .

# Chạy container ngầm
docker run -d \
  --name ethereum-scanner \
  --restart unless-stopped \
  -v $(pwd)/results:/app/results \
  ethereum-scanner

# Chạy với tùy chọn khác
docker run -d \
  --name ethereum-scanner-custom \
  --restart unless-stopped \
  -v $(pwd)/results:/app/results \
  ethereum-scanner \
  python3 ethereum_node_scanner.py --network 1.0.0.0/16 --threads 2000
```

## 📊 Quản lý Services

### Xem logs
```bash
# Xem logs scanner
docker-compose logs -f ethereum-scanner

# Xem logs monitor
docker-compose logs -f monitor

# Xem tất cả logs
docker-compose logs -f
```

### Kiểm tra trạng thái
```bash
# Xem trạng thái containers
docker-compose ps

# Xem resource usage
docker stats
```

### Dừng/Start services
```bash
# Dừng services
docker-compose stop

# Start lại services
docker-compose start

# Restart services
docker-compose restart

# Dừng và xóa containers
docker-compose down
```

## 📁 Kết quả

- **Results**: `./results/ethereum_nodes.json`
- **Logs**: `./logs/`
- **Container logs**: `docker-compose logs`

## 🔧 Tùy chỉnh

### Thay đổi cấu hình quét
Sửa file `docker-compose.yml`:
```yaml
command: >
  python3 ethereum_node_scanner.py 
  --network 1.0.0.0/16  # Thay đổi dải IP
  --timeout 2           # Thay đổi timeout
  --threads 2000        # Thay đổi số threads
  --output /app/results/ethereum_nodes.json
```

### Chạy với dải IP khác
```bash
docker-compose run --rm ethereum-scanner \
  python3 ethereum_node_scanner.py \
  --network 2.0.0.0/16 \
  --threads 1500
```

## 🚀 Tối ưu hiệu suất

### Tăng số threads
```bash
# Trong docker-compose.yml
--threads 5000  # Tối đa threads
```

### Giảm timeout
```bash
# Trong docker-compose.yml
--timeout 0.5   # Timeout nhanh hơn
```

### Quét song song nhiều dải
```bash
# Chạy nhiều containers song song
docker-compose up -d --scale ethereum-scanner=3
```

## 📋 Monitoring

### Real-time monitoring
```bash
# Vào container monitor
docker-compose exec monitor bash

# Chạy monitor script
python3 monitor_scan.py
```

### Kiểm tra kết quả
```bash
# Xem file kết quả
cat results/ethereum_nodes.json | jq

# Đếm số nodes tìm được
cat results/ethereum_nodes.json | jq '.total_nodes_found'
```

## 🛠️ Troubleshooting

### Container không start
```bash
# Xem logs lỗi
docker-compose logs ethereum-scanner

# Rebuild image
docker-compose build --no-cache
```

### Out of memory
```bash
# Giảm số threads
--threads 1000

# Tăng memory limit
docker-compose up -d --memory=4g
```

### Network issues
```bash
# Kiểm tra network
docker network ls
docker network inspect eth_scanner-network
```
