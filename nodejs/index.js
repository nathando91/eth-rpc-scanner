const fs = require('fs');
const https = require('https');
const http = require('http');

// Read the ethereum nodes JSON file
const nodesData = JSON.parse(fs.readFileSync('../results/ethereum_nodes.json', 'utf8'));

// Function to make RPC call to check chainId
async function checkChainId(ip, port) {
    return new Promise((resolve) => {
        const postData = JSON.stringify({
            "jsonrpc": "2.0",
            "method": "eth_chainId",
            "params": [],
            "id": 1
        });

        const options = {
            hostname: ip,
            port: port,
            path: '/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            },
            timeout: 5000 // 5 second timeout
        };

        const req = http.request(options, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                try {
                    const response = JSON.parse(data);
                    resolve({
                        ip: ip,
                        port: port,
                        chainId: response.result,
                        isMainnet: response.result === '0x1',
                        success: true
                    });
                } catch (error) {
                    resolve({
                        ip: ip,
                        port: port,
                        chainId: null,
                        isMainnet: false,
                        success: false,
                        error: 'Invalid JSON response'
                    });
                }
            });
        });

        req.on('error', (error) => {
            resolve({
                ip: ip,
                port: port,
                chainId: null,
                isMainnet: false,
                success: false,
                error: error.message
            });
        });

        req.on('timeout', () => {
            req.destroy();
            resolve({
                ip: ip,
                port: port,
                chainId: null,
                isMainnet: false,
                success: false,
                error: 'Timeout'
            });
        });

        req.write(postData);
        req.end();
    });
}

// Main function to check all nodes
async function checkAllNodes() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `mainnet_nodes_${timestamp}.txt`;

    // Check each node
    for (let i = 0; i < nodesData.nodes.length; i++) {
        const node = nodesData.nodes[i];

        const result = await checkChainId(node.ip, node.port);

        if (result.isMainnet) {
            // Log IP immediately to file
            fs.appendFileSync(filename, `${result.ip}\n`);
        }

        // Small delay to avoid overwhelming the nodes
        await new Promise(resolve => setTimeout(resolve, 100));
    }
}

// Run the check
checkAllNodes().catch(console.error);
