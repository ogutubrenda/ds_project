from flask import Flask, request, jsonify
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
