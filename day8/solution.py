from collections import deque

class Tree:
    def __init__(self, children, meta):
        self.children = children
        self.meta = meta

    def __str__(self):
        return f'{[str(child) for child in self.children]} : {self.meta}'

with open('input.txt', 'r') as f:
    nums = deque(f.readline().strip().split())

def read_tree(nums):
    n_child = int(nums.popleft())
    n_meta = int(nums.popleft())

    children = []
    for _ in range(n_child):
        children.append(read_tree(nums))

    meta = []
    for _ in range(n_meta):
        meta.append(int(nums.popleft()))

    return Tree(children, meta)

# Part 1:
def sum_meta(root):
    child_sum = 0
    for child in root.children:
        child_sum += sum_meta(child)
    return sum(root.meta) + child_sum

#print(sum_meta(read_tree(nums)))

# Part 2:
def sum_complex(root):
    if len(root.children) == 0:
        return sum(root.meta)
    else:
        child_sum = 0
        for meta in root.meta:
            if meta - 1 < len(root.children):
                child_sum += sum_complex(root.children[meta - 1])
        return child_sum

print(sum_complex(read_tree(nums)))
