from flask import Flask, request, jsonify
from consistent_hash import ConsistentHash
import docker

app = Flask(__name__)
ch = ConsistentHash()
client = docker.from_env()

N = 3  # Initial number of servers
servers = [f'Server{i+1}' for i in range(N)]
for server in servers:
    ch.add_node(server)

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({"N": len(ch.nodes)//ch.num_virtual_nodes, "replicas": list(ch.nodes.values())})

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.json
    num_instances = data['n']
    hostnames = data.get('hostnames', [])
    if len(hostnames) > num_instances:
        return jsonify({"message": "Error: Length of hostname list is more than newly added instances", "status": "failure"}), 400
    for i in range(num_instances):
        hostname = hostnames[i] if i < len(hostnames) else f"Server{len(ch.nodes)//ch.num_virtual_nodes + 1}"
        ch.add_node(hostname)
        # Code to spawn a new Docker container can be added here
    return jsonify({"message": {"N": len(ch.nodes)//ch.num_virtual_nodes, "replicas": list(ch.nodes.values())}, "status": "successful"})

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.json
    num_instances = data['n']
    hostnames = data.get('hostnames', [])
    if len(hostnames) > num_instances:
        return jsonify({"message": "Error: Length of hostname list is more than removable instances", "status": "failure"}), 400
    for i in range(num_instances):
        hostname = hostnames[i] if i < len(hostnames) else None
        if hostname:
            ch.remove_node(hostname)
            # Code to remove Docker container can be added here
    return jsonify({"message": {"N": len(ch.nodes)//ch.num_virtual_nodes, "replicas": list(ch.nodes.values())}, "status": "successful"})

@app.route('/<path>', methods=['GET'])
def route_request(path):
    server = ch.get_node(path)
    if server:
        # Code to forward the request to the chosen server
        return jsonify({"message": f"Routed to {server}", "status": "successful"}), 200
    return jsonify({"message": f"Error: '{path}' endpoint does not exist in server replicas", "status": "failure"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
