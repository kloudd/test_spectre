"""
Graph algorithms: BFS, DFS, Dijkstra, topological sort.
"""
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, deque
import heapq


class Graph:
    """Adjacency list graph supporting directed and undirected edges."""

    def __init__(self, directed: bool = False):
        self.directed = directed
        self._adj: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        self._nodes: Set[str] = set()

    def add_edge(self, u: str, v: str, weight: float = 1.0):
        self._adj[u].append((v, weight))
        self._nodes.add(u)
        self._nodes.add(v)
        if not self.directed:
            self._adj[v].append((u, weight))

    @property
    def nodes(self) -> Set[str]:
        return self._nodes.copy()

    def neighbors(self, node: str) -> List[Tuple[str, float]]:
        return self._adj.get(node, [])

    def bfs(self, start: str) -> List[str]:
        """Breadth-first traversal."""
        visited = set()
        order = []
        queue = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor, _ in self._adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start: str) -> List[str]:
        """Depth-first traversal (iterative)."""
        visited = set()
        order = []
        stack = [start]

        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            for neighbor, _ in reversed(self._adj[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
        return order

    def dijkstra(self, start: str) -> Dict[str, float]:
        """Shortest paths from start using Dijkstra's algorithm."""
        dist = {node: float('inf') for node in self._nodes}
        dist[start] = 0
        pq = [(0, start)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in self._adj[u]:
                new_dist = dist[u] + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))
        return dist

    def topological_sort(self) -> Optional[List[str]]:
        """Kahn's algorithm for topological ordering. Returns None if cycle detected."""
        if not self.directed:
            raise ValueError("Topological sort requires a directed graph")

        in_degree = defaultdict(int)
        for node in self._nodes:
            in_degree.setdefault(node, 0)
        for u in self._adj:
            for v, _ in self._adj[u]:
                in_degree[v] += 1

        queue = deque([n for n in self._nodes if in_degree[n] == 0])
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor, _ in self._adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return order if len(order) == len(self._nodes) else None

    def has_cycle(self) -> bool:
        """Detect cycles using DFS coloring."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node: WHITE for node in self._nodes}

        def _dfs(u):
            color[u] = GRAY
            for v, _ in self._adj[u]:
                if color[v] == GRAY:
                    return True
                if color[v] == WHITE and _dfs(v):
                    return True
            color[u] = BLACK
            return False

        return any(_dfs(n) for n in self._nodes if color[n] == WHITE)


if __name__ == "__main__":
    g = Graph(directed=True)
    for u, v, w in [("A","B",4), ("A","C",2), ("B","D",3), ("C","B",1), ("C","D",5), ("D","E",1)]:
        g.add_edge(u, v, w)

    print("BFS:", g.bfs("A"))
    print("DFS:", g.dfs("A"))
    print("Dijkstra:", g.dijkstra("A"))
    print("Topo sort:", g.topological_sort())
    print("Has cycle:", g.has_cycle())
