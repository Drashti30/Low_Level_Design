"""Design a data structure that follows the Least Recently Used (LRU) cache eviction policy.

It should support:

get(key) → return value if key exists, else -1

put(key, value) → insert or update key-value

✅ Both operations must run in O(1) time
✅ When the cache exceeds capacity, evict the least recently used item


Core Idea

We need:

O(1) access to key-value pairs → use a HashMap

O(1) update of usage order → use a Doubly Linked List

Data Structures Used



HashMap - Map keys to their node addresses

Doubly Linked List - Maintain LRU to MRU order

Head = Most Recently Used (MRU)

Tail = Least Recently Used (LRU)

"""



"""“First, I create a Node class to represent each entry in our doubly linked list."""


class Node:
    def __init__(self, key, value):
        self.key = key                  # store key to delete from hashmap when needed
        self.value = value              # actual value
        self.prev = None               # pointer to previous node in list
        self.next = None               # pointer to next node in list

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity            # cache capacity
        self.cache = {}               # hashmap to store key -> node

        # Create dummy head and tail to avoid empty/null checks 
        # Left is least recent used
        # right is most recent used
        self.left = Node(0, 0)         # dummy LRU
        self.right = Node(0, 0)        # dummy MRU
        self.left.next = self.right    # connect LRU to MRU
        self.right.prev = self.left

    def _remove(self, node):
        # unlink a node from its current position
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _insert(self, node):
        # insert a node just before MRU (right dummy)
        prev, nxt = self.right.prev, self.right
        prev.next = nxt.prev = node
        node.prev, node.next = prev, nxt

    def get(self, key):
        if key in self.cache:
            self._remove(self.cache[key])       # move to most recently used
            self._insert(self.cache[key])
            return self.cache[key].value        # return the value
        return -1                               # key not found

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])       # update requires repositioning

        self.cache[key] = Node(key, value)      # add new node
        self._insert(self.cache[key])           # insert to MRU end

        if len(self.cache) > self.cap:
            lru = self.left.next                # least recently used node
            self._remove(lru)                   # remove from list
            del self.cache[lru.key]             # remove from hashmap


"""
🧪 Dry Run

cache = LRUCache(2)
cache.put(1, 1)  # cache = {1}
cache.put(2, 2)  # cache = {2, 1}
cache.get(1)     # return 1, cache = {1, 2}
cache.put(3, 3)  # evict key 2 → cache = {3, 1}
cache.get(2)     # return -1

Explanation:

After put(1,1) and put(2,2) → cache is [2,1] (MRU left side)

get(1) makes 1 most recent → [1,2]

put(3,3) causes capacity overflow, evict LRU = 2 → [3,1]

get(2) → returns -1

Time Complexcity - O(1) - both the operations 
Space Complexcity - O(N) - both the operations 

"""


if __name__ == "__main__":
    cache = LRUCache(4)  # Capacity = 2

    cache.put(1, 1)      # Cache = {1=1}
    cache.put(2, 2)      # Cache = {1=1, 2=2}
    print(cache.get(1))  # Returns 1, Cache = {2=2, 1=1}

    cache.put(3, 3)      # Evicts key 2, Cache = {1=1, 3=3}
    print(cache.get(2))  # Returns -1 (not found)
    print(cache.get(3))  # Returns 3
    print(cache.get(1))  # Returns 1
    cache.put(4, 4)      # Evicts key 3, Cache = {1=1, 4=4}
    print(cache.get(3))  # Returns -1
    print(cache.get(4))  # Returns 4

    print(cache.get(5)) 