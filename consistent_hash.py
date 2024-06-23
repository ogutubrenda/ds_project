import hashlib
import bisect

class ConsistentHash:
    def __init__(self, num_slots=512, num_virtual_nodes=9):
        self.num_slots = num_slots
        self.num_virtual_nodes = num_virtual_nodes
        self.ring = []
        self.nodes = {}
        
    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % self.num_slots
    
    def add_node(self, node):
        for i in range(self.num_virtual_nodes):
            virtual_node = f"{node}_{i}"
            position = self._hash(virtual_node)
            self.ring.append(position)
            self.nodes[position] = node
        self.ring.sort()
    
    def remove_node(self, node):
        for i in range(self.num_virtual_nodes):
            virtual_node = f"{node}_{i}"
            position = self._hash(virtual_node)
            self.ring.remove(position)
            del self.nodes[position]
    
    def get_node(self, key):
        if not self.ring:
            return None
        position = self._hash(key)
        index = bisect.bisect_right(self.ring, position)
        if index == len(self.ring):
            index = 0
        return self.nodes[self.ring[index]]

# Example usage
if __name__ == '__main__':
    ch = ConsistentHash()
    ch.add_node('Server1')
    ch.add_node('Server2')
    ch.add_node('Server3')
    print(ch.get_node('client_request_1'))
