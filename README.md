# Ethereum Node Scanner

Python script để quét tìm tất cả các Ethereum nodes đang chạy trên port 8545 và phản hồi JSON-RPC `eth_syncing`.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Sử dụng

### 1. Quét các mạng private thông thường (mặc định)
```bash
python ethereum_node_scanner.py --common
```

### 2. Quét một mạng cụ thể
```bash
python ethereum_node_scanner.py --network 192.168.1.0/24
```

### 3. Quét một dải IP cụ thể
```bash
python ethereum_node_scanner.py --ip-range 192.168.1.1 192.168.1.254
```

### 4. Tùy chỉnh timeout và số thread
```bash
python ethereum_node_scanner.py --common --timeout 5 --threads 500
```

### 5. Lưu kết quả vào file cụ thể
```bash
python ethereum_node_scanner.py --common --output my_scan_results.json
```

## Các tùy chọn

- `--network`: Quét một mạng cụ thể (ví dụ: 192.168.1.0/24)
- `--ip-range`: Quét một dải IP cụ thể (ví dụ: 192.168.1.1 192.168.1.254)
- `--common`: Quét các mạng private thông thường (192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, 127.0.0.0/8)
- `--timeout`: Thời gian timeout cho mỗi kết nối (mặc định: 3 giây)
- `--threads`: Số thread tối đa (mặc định: 1000)
- `--output`: Tên file để lưu kết quả

## Kết quả

Script sẽ:
1. Hiển thị các nodes được tìm thấy trong quá trình quét
2. Lưu tất cả kết quả vào file JSON với timestamp
3. Hiển thị tóm tắt cuối cùng

## Ví dụ kết quả

```
✓ Found Ethereum node: 192.168.1.100:8545
  Response: {'jsonrpc': '2.0', 'id': 1, 'result': False}

✓ Found Ethereum node: 10.0.0.50:8545
  Response: {'jsonrpc': '2.0', 'id': 1, 'result': True}
```

## Lưu ý

- Script sử dụng multithreading để quét nhanh
- Mặc định quét các mạng private để tránh quét internet
- Kết quả được lưu tự động với timestamp
- Có thể tùy chỉnh timeout và số thread tùy theo mạng
# eth-rpc-scanner
