N = 3  # Number of server containers
num_slots = 512  # Total slots in the hash map
K = 9  # Number of virtual servers per container

# Hash functions
def hash_request(request_id):
    return (request_id ** 2 + 2 * request_id + 17) % num_slots

def hash_server(server_id, virtual_server_id):
    return (server_id + virtual_server_id + 2 * virtual_server_id + 25) % num_slots

# Initialize the hash map
hash_map = [None] * num_slots

# Add server containers to the hash map
for server_id in range(N):
    for virtual_server_id in range(K):
        add_to_hash_map(server_id, virtual_server_id)

# Handle hash collisions
def add_to_hash_map(server_id, virtual_server_id):
    slot = hash_server(server_id, virtual_server_id)
    while hash_map[slot] is not None and hash_map[slot] != server_id:
        slot = (slot + 1) % num_slots
    hash_map[slot] = server_id

# Map requests to server containers
def map_request(request_id):
    slot = hash_request(request_id)
    while hash_map[slot] is None:
        slot = (slot + 1) % num_slots
    return hash_map[slot]

# Test the implementation
requests = [123456, 789012, 345678]
for request_id in requests:
    server_id = map_request(request_id)
    print(f"Request {request_id} is mapped to Server {server_id}")