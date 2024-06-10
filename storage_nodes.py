import hashlib
import bisect
from bisect import bisect_left, bisect_right


class StorageNode:
    def __init__(self, name, host):
        self.name = name
        self.host = host

    def put_file(self, path):
        print(f"Putting file {path} on node {self.name} ({self.host})")
        # Add your implementation for putting the file on the storage node

    def fetch_file(self, path):
        print(f"Fetching file {path} from node {self.name} ({self.host})")
        # Add your implementation for fetching the file from the storage node

storage_nodes = [
    StorageNode(name='A', host='10.131.213.12'),
    StorageNode(name='B', host='10.131.217.11'),
    StorageNode(name='C', host='10.131.142.46'),
    StorageNode(name='D', host='10.131.114.17'),
    StorageNode(name='E', host='10.131.189.18'),

]


def hash_fn(key):
    """The function sums the bytes present in the 'key' and then take a mod ith 5. This hash function thus generates output in the range [0,4].
    """
    return sum(bytearray(key.encode('utf-8'))) % 5

def upload(path):
    # We use the hash function to get the index of the storage node
    #that would hold the file
    index = hash_fn(path)

    # we get the StorageNode instance
    node = storage_nodes[index]

    # we put the file on the node and return
    return node.put_file(path)

def fetch(path):
    # we use the hash function to get the index of the storage node
    # that would hold the file
    index = hash_fn(path)

    # we get the StorageNode instance
    node = storage_nodes[index]

    # we fetch the file from the node and return
    return node.fetch_file(path)

def hash_fn(key: str, total_slots: int) -> int:
    """ hash fn creates an integer equivalent of a SHA26 hash and takes
    a modulo with the total number of slots in hash space.
    """
    hsh = hashlib.sha256()
    # converting data into bytes and passing it to a hash function
    hsh.update(bytes (key.encode('utf-8')))

    #converting the HEX digest into equivalent integer value 
    return int(hsh.hexdigest(), 16) % total_slots

def add_node(self, node: StorageNode) -> int:
    """add_node function adds a new node in the system and returns the key
    from the hash space where it was placed 
    """
    # handling error when hash space is full.
    if len(self._keys) == self.total_slots:
        raise Exception("hash space is full")
    
    key = hash_fn(node.host, self.total_hosts)

    # find the index where the key should be inserted in the keys array
    # this will be the index where the storage node will be added in the nodes array

    index = bisect(self._keys, key)

    # if we have already seen the key i.e. node already is present 
    # for the same key, we raise collision Exception
    if index > 0 and self._keys[index -1] == key:
        raise Exception("collision occured")
    
    # Perform data migration

    # insert the node_id and the key at the same 'index' location.
    # this insertion will keep nodes and keys sorted w.r.t keys.
    self.nodes.insert(index, node)
    self._keys.insert(index, key)

    return key

def remove_node(self, node: StorageNode) -> int:
    """remove_node removes the node and returns the key
    from the hash space on which the node was placed.
    """

    # handling error when space is empty
    if len(self._keys) == 0:
        raise Exception("hash space is empty")

    key = hash_fn(node.host, self.total_slots)

    # we find the index where the key would reside in the keys
    index = bisect_left(self._keys, key)

    # if key does not exist in the array we raise Exception
    if index >= len(self._keys) or self._keys[index] != key:
        raise Exception("node does not exist")

    # Perform data migration

    # now that all sanity checks are done we popping the
    # keys and nodes at the index and thus removing the presence of the node.
    self._keys.pop(index)
    self.nodes.pop(index)

    return key

def assign(self, item: str) -> str:
    """Given an item, the function returns the node it is associated with.
    """
    key = hash_fn(item, self.total_slots)

    # we find the first node to the right of this key
    # if bisect_right returns index which is out of bounds then
    # we circle back to the first in the array in a circular fashion.
    index = bisect_right(self._keys, key) % len(self._keys)

    # return the node present at the index
    return self.nodes[index]