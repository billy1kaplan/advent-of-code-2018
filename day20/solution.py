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
    seen = set()
    costs = {0: 0}
    max_cost = 0
    while len(queue) > 0:
        head, cost = queue.popleft()
        costs[head] = cost
        neighbors = graph[head]
        unseen = neighbors - seen

        for n in unseen:
            seen.add(n)
            queue.append((n, cost + 1))
    return costs

class Option:
    def _travel(self, start, cur_start, handle):
        return start

    def __str__(self):
        return '|'

class Path:
    def __init__(self, path):
        self.path = path

    def _travel(self, start, cur_start, handle):
        prev, offset = 0, 0
        for ch in self.path:
            offset += offsets[ch]
            handle(cur_start + prev, cur_start + offset)
            prev = offset
        return cur_start + offset

    def __str__(self):
        return f'Path = {self.path}'

class TreeNode:
    def __init__(self, exp):
        self.exp = exp

    def travel(self, start, handle):
        return self._travel(start, start, handle)

    def _travel(self, start, cur_start, handle):
        points = cur_start
        for move in self.exp:
            points = move._travel(cur_start, points, handle)
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
    elif head == '|':
        return (Option(), tail)
    elif head == ')':
        raise ValueError('Unexpected end of regular expression')
    else:
        return (Path(head), tail)

with open('input.txt', 'r') as f:
    regex = f.readline().strip()
    tokens = tokenize(regex)
    regex_tree = parse(tokens)
    regex_tree.travel(0, handler)
    bfs_res = bfs(graph)
    print('Part 1 =', max(bfs_res.values()))
    print('Part 2 =', len([res for res in bfs_res.values() if res >= 1000]))
