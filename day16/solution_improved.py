from collections import namedtuple, defaultdict

# Problem Set Up:
add = lambda x, y: x + y
prod = lambda x, y: x * y
band = lambda x, y: x & y
bor = lambda x, y: x | y
gt = lambda x, y: 1 if x > y else 0
eq = lambda x, y: 1 if x == y else 0

# Small (probably unnecessary) abstractions for making functions on registers
# Follows a similar naming convention to the problem statement on AoC
# These make deep copies to not mutate the original registers
def rrfunc(A, B, C, init, bin_op):
    result = init[::]
    result[C] = bin_op(init[A], init[B])
    return result

def irfunc(A, B, C, init, bin_op):
    result = init[::]
    result[C] = bin_op(A, init[B])
    return result

def rifunc(A, B, C, init, bin_op):
    result = init[::]
    result[C] = bin_op(init[A], B)
    return result

# All of the opcodes
ops = [
    lambda A, B, C, init: rrfunc(A, B, C, init, add),
    lambda A, B, C, init: rifunc(A, B, C, init, add),
    lambda A, B, C, init: rrfunc(A, B, C, init, prod),
    lambda A, B, C, init: rifunc(A, B, C, init, prod),
    lambda A, B, C, init: rrfunc(A, B, C, init, band),
    lambda A, B, C, init: rifunc(A, B, C, init, band),
    lambda A, B, C, init: rrfunc(A, B, C, init, bor),
    lambda A, B, C, init: rifunc(A, B, C, init, bor),
    lambda A, B, C, init: rrfunc(A, B, C, init, lambda a, b: a),
    lambda A, B, C, init: irfunc(A, B, C, init, lambda a, b: a),
    lambda A, B, C, init: irfunc(A, B, C, init, gt),
    lambda A, B, C, init: rifunc(A, B, C, init, gt),
    lambda A, B, C, init: rrfunc(A, B, C, init, gt),
    lambda A, B, C, init: irfunc(A, B, C, init, eq),
    lambda A, B, C, init: rifunc(A, B, C, init, eq),
    lambda A, B, C, init: rrfunc(A, B, C, init, eq)
]

Instruction = namedtuple('Instruction', ['opcode', 'A', 'B', 'C'])
Sample = namedtuple('Sample', ['before', 'instruction', 'after'])

# Recursive Back Tracking To Solve Part 2
# Input: [(0, [F1, F2, F3]), (1, [F2, F3]) ...]
# Returns [(0, F1), (1, F3), ...] or False if a solution does not exist
def solve(code_to_functions):

    # Checks if all of the mappings are distinct
    def distinct(codes):
        return len(codes) == len(set([f for _, f in codes]))

    # Try using first encountered mapping if possible
    # Try the rest if this fails and recurse
    def _iter(remaining, selected):
        if remaining == []:
            return selected
        else:
            first = remaining[0]
            rest = remaining[1:]

            code, amb = first

            for f in amb:
                attempt = selected + [(code, f)]
                if distinct(attempt):
                    result = _iter(rest, attempt)
                    if result:
                        return result

            return False

    return _iter(code_to_functions, [])

# Super ugly parsing
with open('input.txt', 'r') as f:
    lines = f.readlines()
    instructions = []

    index = 0
    gt3 = 0
    operations = defaultdict(set)
    while True:
        before = lines[index].strip()
        op = lines[index + 1].strip()
        after = lines[index + 2].strip()

        # Hit the second part of the file
        if 'Before:' not in before:
            break

        before_state = eval(before.split('Before: ')[1])
        instruction = list(map(int, op.split()))
        after_state = eval(after.split('After:  ')[1])

        opcode = instruction[0]
        registers = instruction[1:]

        amb = set()
        count = 0
        for fop in ops:
            if fop(*registers, before_state) == after_state:
                count += 1
                amb.add(fop)

        if count >= 3:
            gt3 += 1

        operations[opcode] = operations[opcode].union(amb)
        index += 4

    print('Part 1: ', gt3)

    # Solve for the opcode to function mappings
    amb = [(code, list(ops)) for code, ops in operations.items()]

    # Pack the mappings into a dictionary for easier lookup
    decoded = { code : f for code, f in solve(amb) }

    # Ignore empty lines
    part2 = [list(map(int, line.strip().split())) for line in lines[index:] if line.strip()]

    state = [0, 0, 0, 0]
    for inst in part2:
        opcode = inst[0]
        registers = inst[1:]

        f_for_code = decoded[opcode]
        state = f_for_code(*registers, state)

    print('Part 2: ', state[0])
