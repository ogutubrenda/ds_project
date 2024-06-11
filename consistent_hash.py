#Implement a consistent hash map data structure using the provided parameters:
# - Number of server containers (N) = 3
#- Total slots in hash map = 512
#- Number of virtual servers per container (K) = log2(512) = 9
#- Hash functions: H(i) = (i^2 + 2i + 17) % 512, Φ(i, j) = (i + j + 2j + 25) % 512

N = 3  # Number of server containers
num_slots = 512  # Total slots in the hash map
K = 9  # Number of virtual servers per container

# Hash functions
def hash_request(request_id):
    return (request_id ** 2 + 2 * request_id + 17) % num_slots

def hash_server(server_id, virtual_server_id):
    return (str(server_id) + str(virtual_server_id) + str(2 * virtual_server_id) + "25") % num_slots

class ConsistentHashMap:
    def __init__(self, num_slots, num_servers, num_virtual_servers):
        self.num_slots = num_slots
        self.num_servers = num_servers
        self.num_virtual_servers = num_virtual_servers
        self.hash_map = [None] * num_slots

    def add_server(self, server_id):
        for virtual_server_id in range(self.num_virtual_servers):
            self.add_to_hash_map(server_id, virtual_server_id)

    def add_to_hash_map(self, server_id, virtual_server_id):
        slot = hash_server(server_id, virtual_server_id)
        while self.hash_map[slot] is not None and self.hash_map[slot] != server_id:
            slot = (slot + 1) % self.num_slots
        self.hash_map[slot] = server_id

    def remove_server(self, server_id):
        for virtual_server_id in range(self.num_virtual_servers):
            self.remove_from_hash_map(server_id, virtual_server_id)

    def remove_from_hash_map(self, server_id, virtual_server_id):
        slot = hash_server(server_id, virtual_server_id)
        while self.hash_map[slot] != server_id:
            slot = (slot + 1) % self.num_slots
        self.hash_map[slot] = None

    def map_request(self, request_id):
        slot = hash_request(request_id)
        while self.hash_map[slot] is None:
            slot = (slot + 1) % self.num_slots
        return self.hash_map[slot]