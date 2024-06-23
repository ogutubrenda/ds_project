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
    server_id_str = str(server_id)
    virtual_id_str = str(virtual_id)
    return (server_id_str + virtual_id_str + str(2 ** virtual_id) + str(25)) % self.num_slots

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
if __name__ == "__main__":
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
