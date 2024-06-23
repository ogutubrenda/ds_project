<<<<<<< HEAD
import math

class ConsistentHashMap:
    def __init__(self, num_servers, num_slots, num_virtual_servers):
        self.num_servers = num_servers
        self.num_slots = num_slots
        self.num_virtual_servers = num_virtual_servers
        self.slots = [-1] * num_slots
        self.server_map = {}

        self._initialize_virtual_servers()

    def _hash_request(self, request_id):
        return (request_id + (2 ** request_id) + 17) % self.num_slots

    def _hash_virtual_server(self, server_id, virtual_id):
        return (server_id + virtual_id + (2 ** virtual_id) + 25) % self.num_slots

    def _initialize_virtual_servers(self):
        for server_id in range(self.num_servers):
            self.server_map[server_id] = []
            for virtual_id in range(self.num_virtual_servers):
                slot = self._hash_virtual_server(server_id, virtual_id)
                while self.slots[slot] != -1:
                    slot = (slot + 1) % self.num_slots  # Linear probing for collision resolution
                self.slots[slot] = server_id
                self.server_map[server_id].append(slot)

    def add_server(self, new_server_id):
        self.server_map[new_server_id] = []
        for virtual_id in range(self.num_virtual_servers):
            slot = self._hash_virtual_server(new_server_id, virtual_id)
            while self.slots[slot] != -1:
                slot = (slot + 1) % self.num_slots  # Linear probing for collision resolution
            self.slots[slot] = new_server_id
            self.server_map[new_server_id].append(slot)

    def remove_server(self, server_id):
        for slot in self.server_map[server_id]:
            self.slots[slot] = -1
        del self.server_map[server_id]

    def get_server_for_request(self, request_id):
        request_slot = self._hash_request(request_id)
        for i in range(self.num_slots):
            slot = (request_slot + i) % self.num_slots
            if self.slots[slot] != -1:
                return self.slots[slot]
        return None

# Example Usage:
num_servers = 3
num_slots = 512
num_virtual_servers = 9

hash_map = ConsistentHashMap(num_servers, num_slots, num_virtual_servers)

# Adding a new server
hash_map.add_server(3)

# Removing a server
hash_map.remove_server(2)

# Getting the server for a request
request_id = 132574
assigned_server = hash_map.get_server_for_request(request_id)
print(f"Request {request_id} is handled by server {assigned_server}")

# Debugging output to see slot assignments
print("Slot assignments:")
for i, server in enumerate(hash_map.slots):
    if server != -1:
        print(f"Slot {i} -> Server {server}")
=======
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
>>>>>>> 2c6a64807b6fc0c15f4b2a007dc62bd5eef014e8
