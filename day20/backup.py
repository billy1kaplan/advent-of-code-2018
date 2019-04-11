from collections import deque, defaultdict

offsets = { 'E' : 1,
            'W' : -1,
            'N' : 1j,
            'S' : -1j }

graph = defaultdict(set)
def handler(start, end):
    graph[start].add(end)

def bfs(graph):
    queue = deque([(0, 0)])
    seen = set([0])
    max_cost = 0
    while len(queue) > 0:
        head, cost = queue.popleft()
        max_cost = max(max_cost, cost)
        neighbors = graph[head]
        unseen = neighbors - seen

        for n in unseen:
            seen.add(n)
            queue.append((n, cost + 1))
    return max_cost

class Path:
    def __init__(self, paths):
        self.paths = paths

    def travel(self, start, handle):
        return [self.walk_start(point, path, handle) for path in self.paths for point in start]

    def walk_start(self, start, path, handle):
        prev, offset = 0, 0
        for ch in path:
            offset += offsets[ch]
            handle(start + prev, start + offset)
            prev = offset
        return start + offset

    def __str__(self):
        return f'Path = {self.paths}'

class TreeNode:
    def __init__(self, exp):
        self.exp = exp

    def travel(self, start, handle):
        points = start
        for move in self.exp:
            points = move.travel(points, handle)
        return points

    def __str__(self):
        return f'TreeNode = {str(list(map(str, self.exp)))}'

def tokenize(s):
    return s.replace('^', '(')\
            .replace('$', ')')\
            .replace('|', ' | ')\
            .replace('(', ' ( ')\
            .replace(')', ' ) ')\
            .split()

def parse(s):
    parse_tree, _ = _parse(s)
    return parse_tree

def _parse(s):
    head = s[0]
    tail = s[1:]

    if head == '(':
        sub_tree = []
        while head != ')':
            parsed, tail = _parse(tail)
            head = tail[0]
            sub_tree.append(parsed)
        return (TreeNode(sub_tree), tail[1:])
    elif head == ')':
        raise ValueError('Unexpected end of regular expression')
    else:
        return (Path(head.split('|')), tail)
        

with open('example2.txt', 'r') as f:
    regex = f.readline().strip()
    tokens = tokenize(regex)
    print(tokens)
    regex_tree = parse(tokens)
    print(regex_tree)
    regex_tree.travel([0], handler)
    #print('Part 1 =', max(visited.values()))
    #print(graph)
    print(bfs(graph))
