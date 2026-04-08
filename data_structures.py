"""
Core data structures: LinkedList, Stack, Queue, LRU Cache.
"""
from typing import Any, Optional
from collections import OrderedDict


class Node:
    __slots__ = ('val', 'next', 'prev')

    def __init__(self, val: Any, next_node=None, prev_node=None):
        self.val = val
        self.next = next_node
        self.prev = prev_node


class LinkedList:
    """Doubly linked list with O(1) append/prepend."""

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size = 0

    def append(self, val: Any):
        node = Node(val, prev_node=self.tail)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self._size += 1

    def prepend(self, val: Any):
        node = Node(val, next_node=self.head)
        if self.head:
            self.head.prev = node
        else:
            self.tail = node
        self.head = node
        self._size += 1

    def remove(self, val: Any) -> bool:
        curr = self.head
        while curr:
            if curr.val == val:
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next
                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev
                self._size -= 1
                return True
            curr = curr.next
        return False

    def to_list(self) -> list:
        result = []
        curr = self.head
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result

    def __len__(self):
        return self._size

    def __contains__(self, val):
        curr = self.head
        while curr:
            if curr.val == val:
                return True
            curr = curr.next
        return False


class Stack:
    """LIFO stack backed by a list."""

    def __init__(self):
        self._items: list = []

    def push(self, item: Any):
        self._items.append(item)

    def pop(self) -> Any:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


class Queue:
    """FIFO queue using two stacks for amortized O(1) operations."""

    def __init__(self):
        self._inbox = Stack()
        self._outbox = Stack()

    def enqueue(self, item: Any):
        self._inbox.push(item)

    def dequeue(self) -> Any:
        if self._outbox.is_empty:
            while not self._inbox.is_empty:
                self._outbox.push(self._inbox.pop())
        if self._outbox.is_empty:
            raise IndexError("dequeue from empty queue")
        return self._outbox.pop()

    @property
    def is_empty(self) -> bool:
        return self._inbox.is_empty and self._outbox.is_empty

    def __len__(self):
        return len(self._inbox) + len(self._outbox)


class LRUCache:
    """Least Recently Used cache with O(1) get/put."""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self._cache: OrderedDict = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: Any) -> Optional[Any]:
        if key in self._cache:
            self._cache.move_to_end(key)
            self.hits += 1
            return self._cache[key]
        self.misses += 1
        return None

    def put(self, key: Any, value: Any):
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def __len__(self):
        return len(self._cache)

    def __contains__(self, key):
        return key in self._cache
