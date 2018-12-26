from collections import namedtuple, defaultdict

Instruction = namedtuple('Instruction', ['opcode', 'A', 'B', 'C'])
Sample = namedtuple('Sample', ['before', 'instruction', 'after'])

add = lambda x, y: x + y
prod = lambda x, y: x * y
band = lambda x, y: x & y
bor = lambda x, y: x | y
gt = lambda x, y: 1 if x > y else 0
eq = lambda x, y: 1 if x == y else 0

def rfunc(A, B, C, init, bin_op):
    result = init[:]
    result[C] = bin_op(init[A], init[B])
    return result

def afunc(A, B, C, init, bin_op):
    result = init[:]
    result[C] = bin_op(A, init[B])
    return result

def vfunc(A, B, C, init, bin_op):
    result = init[:]
    result[C] = bin_op(init[A], B)
    return result

def addr(A, B, C, init):
    return rfunc(A, B, C, init, add)

def addi(A, B, C, init):
    return vfunc(A, B, C, init, add)

def mulr(A, B, C, init):
    return rfunc(A, B, C, init, prod)

def muli(A, B, C, init):
    return vfunc(A, B, C, init, prod)

def banr(A, B, C, init):
    return rfunc(A, B, C, init, band)

def bani(A, B, C, init):
    return vfunc(A, B, C, init, band)

def borr(A, B, C, init):
    return rfunc(A, B, C, init, bor)

def bori(A, B, C, init):
    return vfunc(A, B, C, init, bor)

def setr(A, B, C, init):
    return rfunc(A, B, C, init, lambda a, b: a)

def seti(A, B, C, init):
    return afunc(A, B, C, init, lambda a, b: a)

def gtir(A, B, C, init):
    return afunc(A, B, C, init, gt)

def gtri(A, B, C, init):
    return vfunc(A, B, C, init, gt)

def gtrr(A, B, C, init):
    return rfunc(A, B, C, init, gt)

def eqir(A, B, C, init):
    return afunc(A, B, C, init, eq)

def eqri(A, B, C, init):
    return vfunc(A, B, C, init, eq)

def eqrr(A, B, C, init):
    return rfunc(A, B, C, init, eq)

ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

def solve(amb):
    def distinct(codes):
        return len(codes) == len(set([f for _, f in codes]))

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
    return _iter(amb, [])

with open('input.txt', 'r') as f:
    lines = f.readlines()
    instructions = []

    index = 0

    operations = defaultdict(set)

    while True:
        before = lines[index].strip()
        op = lines[index + 1].strip()
        after = lines[index + 2].strip()

        if 'Before:' not in before:
            break

        before_state = eval(before.split('Before: ')[1])
        instruction = Instruction._make(list(map(int, op.split())))
        after_state = eval(after.split('After:  ')[1])

        amb = set()
        for fop in ops:
            if fop(getattr(instruction, 'A'), getattr(instruction, 'B'), getattr(instruction, 'C'), before_state) == after_state:
                amb.add(fop)

        operations[getattr(instruction, 'opcode')] = operations[getattr(instruction, 'opcode')].union(amb)
        index += 4


    amb = [(code, list(ops)) for code, ops in operations.items()]
    decoded = { code : f for code, f in solve(amb) }

    part2 = [Instruction._make(list(map(int, line.strip().split()))) for line in lines[index:] if line.strip()]
    registers = [0, 0, 0, 0]
    print(part2)

    for inst in part2:
        f_for_code = decoded[getattr(inst, 'opcode')]
        registers = f_for_code(getattr(inst, 'A'), getattr(inst, 'B'), getattr(inst, 'C'), registers)

    print('Part 2: ', registers[0])
