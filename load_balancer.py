from flask import Flask, request, jsonify
<<<<<<< HEAD
import docker
from consistent_hash import ConsistentHashMap  # Assuming ConsistentHashMap is implemented in consistent_hash.py

app = Flask(__name__)
client = docker.from_env()

# Example parameters for consistent hashing
num_servers = 10
num_slots = 100
num_virtual_servers = 1

hash_ring = ConsistentHashMap(num_servers, num_slots, num_virtual_servers)

servers = []

def start_server(server_id):
    container = client.containers.run(
        "web_server",
        environment={"SERVER_ID": server_id},
        detach=True,
        name=server_id
    )
    return container

def stop_server(container):
    container.stop()
    container.remove()

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        "N": len(servers),
        "replicas": servers
    }), 200

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.json
    num_instances = data.get("n", 1)
    hostnames = data.get("hostnames", [])

    new_servers = []
    for i in range(num_instances):
        server_id = hostnames[i] if i < len(hostnames) else f"Server_{len(servers) + i + 1}"
        container = start_server(server_id)
        hash_ring.add_server(server_id)
        servers.append(server_id)
        new_servers.append(server_id)
    
    return jsonify({
        "message": {
            "N": len(servers),
            "replicas": servers
        },
        "status": "successful"
    }), 200

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.json
    num_instances = data.get("n", 1)
    hostnames = data.get("hostnames", [])

    for i in range(num_instances):
        if hostnames and i < len(hostnames):
            server_id = hostnames[i]
        else:
            server_id = servers.pop()
        
        hash_ring.remove_server(server_id)
        container = client.containers.get(server_id)
        stop_server(container)
        servers.remove(server_id)
    
    return jsonify({
        "message": {
            "N": len(servers),
            "replicas": servers
        },
        "status": "successful"
    }), 200

@app.route('/<path:path>', methods=['GET'])
def proxy_request(path):
    server_id = hash_ring.get_server(path)
    server_container = client.containers.get(server_id)
    # You will need to implement the request forwarding logic here.
    return jsonify({"message": f"Request forwarded to {server_id}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
=======
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
>>>>>>> 2c6a64807b6fc0c15f4b2a007dc62bd5eef014e8
