from collections import defaultdict, deque, Counter

class Graph:
    def __init__(self):
        self._graph = defaultdict(set)

    def vertices(self):
        return self._graph.keys()

    def edges(self):
        for v, outgoing in self._graph.items():
            for out in outgoing:
                yield (v, out)

    def count_incident(self):
        result = Counter()
        for v, outgoing in self._graph.items():
            if v not in result:
                result[v] = 0
            for out in outgoing:
                result[out] += 1
        return result

    def add_edge(self, v1, v2):
        self._graph[v1].add(v2)
        self._graph[v2] # Initialize to empty if not present

    def neighbors(self, v):
        return self._graph[v]

    def __str__(self):
        return '\n'.join([f'{v} : {incident}' for v, incident in self._graph.items()])

def topological_sort(graph):
    order = []
    degrees = graph.count_incident()
    queue = deque([vertex for vertex, incident in degrees.items() if incident == 0])

    while queue:
        free_vertex = queue.popleft()
        order.append(free_vertex)

        for neighbor in graph.neighbors(free_vertex):
            degrees[neighbor] -= 1
            if degrees[neighbor] == 0:
                queue.append(neighbor)
    return order

A = 'A'
B = 'B'
C = 'C'
D = 'D'
E = 'E'

g = Graph()

g.add_edge(A, B)
g.add_edge(B, C)
g.add_edge(B, D)
g.add_edge(D, E)

print(topological_sort(g))
