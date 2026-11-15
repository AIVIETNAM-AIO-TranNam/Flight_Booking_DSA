class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

class HashTable:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self._hash(key)
        for kv in self.table[index]:
            if kv[0] == key:
                kv[1] = value
                return
        self.table[index].append([key, value])

    def get(self, key):
        index = self._hash(key)
        for kv in self.table[index]:
            if kv[0] == key:
                return kv[1]
        return None

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def enqueue_with_priority(self, item, priority):
        self.heap.append((priority, item))
        self._heapify_up(len(self.heap) - 1)

    def dequeue_highest_priority(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()[1]
        root = self.heap[0][1]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, i):
        p = (i - 1) // 2
        if i > 0 and self.heap[i][0] > self.heap[p][0]:
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            self._heapify_up(p)

    def _heapify_down(self, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < len(self.heap) and self.heap[l][0] > self.heap[largest][0]:
            largest = l
        if r < len(self.heap) and self.heap[r][0] > self.heap[largest][0]:
            largest = r
        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self._heapify_down(largest)