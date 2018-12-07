import re

def remove_dependency(graph, dependency):
    for item, dependencies in graph.items():
        if dependency in dependencies:
            graph[item].remove(dependency)

def compute_cost(item):
    return 61 + ord(item) - ord('A')

with open('input.txt', 'r') as f:
    lines = f.readlines()

graph = {}
step_extract = re.compile(r'(?:[S|s]tep) (\w+)')
for line in lines:
    step1, step2  = re.findall(step_extract, line)

    if step1 not in graph:
        graph[step1] = set()
    if step2 not in graph:
        graph[step2] = set()
    graph[step2].add(step1)

ordering = []
print(graph)
while len(ordering) < len(graph.keys()):
    dependency = None
    for item, dependencies in graph.items():
        if len(dependencies) == 0 and not item in ordering:
            if dependency is None or dependency > item:
                dependency = item

    ordering.append(dependency)
    remove_dependency(graph, dependency)
print("Ordering: ", ''.join(ordering))

# Part 2
graph = {}
costs = {}
for line in lines:
    step1, step2  = re.findall(step_extract, line)

    if step1 not in graph:
        costs[step1] = compute_cost(step1)
        graph[step1] = set()
    if step2 not in graph:
        costs[step2] = compute_cost(step2)
        graph[step2] = set()
    graph[step2].add(step1)

time = 0
completed = []
n_workers = 5
workers = { i : None for i in range(n_workers) }
while len(completed) < len(graph.keys()):
    in_progress = []
    for item, dependencies in graph.items():
        if len(dependencies) == 0 and not item in completed:
            in_progress.append(item)

    sorted_tasks = sorted(in_progress)
    available_tasks = [task for task in sorted_tasks if task not in workers.values()]
    available_workers = [worker for worker, task in workers.items() if not task]

    for worker, task in workers.items():
        if task:
            if costs[task] == 1:
                completed.append(task)
                remove_dependency(graph, task)
                workers[worker] = None
            else:
                costs[task] -= 1

    for worker, task in zip(available_workers, available_tasks):
        workers[worker] = task
        if costs[task] == 1:
            completed.append(task)
            remove_dependency(graph, task)
            workers[worker] = None
        else:
            costs[task] -= 1

    time += 1
print("Time Elapsed", time)
