from flask import Flask, request, jsonify
import consistent_hash

app = Flask(__name__)

servers = []
consistent_hash_map = consistent_hash.ConsistentHashMap(num_slots=512, num_servers=3, num_virtual_servers=9)

for i in range(3):
    server_id = f"Server {i+1}"
    servers.append(server_id)
    consistent_hash_map.add_server(server_id)

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({"replicas": servers})

@app.route('/add', methods=['POST'])
def add_servers():
    data = request.get_json()
    n = data.get('n')
    hostnames = data.get('hostnames', [])

    if len(hostnames) > n:
        return jsonify({"error": "Length of hostname list is more than newly added instances"}), 400

    for i in range(n):
        server_id = hostnames[i] if i < len(hostnames) else f"Server {len(servers) + 1}"
        servers.append(server_id)
        consistent_hash_map.add_server(server_id)

    return jsonify({"replicas": servers})

@app.route('/rm', methods=['DELETE'])
def remove_servers():
    data = request.get_json()
    n = data.get('n')
    hostnames = data.get('hostnames', [])

    if len(hostnames) > n:
        return jsonify({"error": "Length of hostname list is more than removable instances"}), 400

    for hostname in hostnames:
        if hostname in servers:
            servers.remove(hostname)
            consistent_hash_map.remove_server(hostname)

    return jsonify({"replicas": servers})

@app.route('/<path>', methods=['GET'])
def route_request(path):
    request_id = request.environ.get('HTTP_X_REQUEST_ID', '123456')
    server_id = consistent_hash_map.map_request(request_id)
    # Implement logic to forward the request to the server instance
    return f"Request for /{path} routed to {server_id}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)