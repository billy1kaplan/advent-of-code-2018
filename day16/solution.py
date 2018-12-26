from collections import namedtuple

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

with open('input.txt', 'r') as f:
    lines = f.readlines()
    instructions = []

    index = 0
    gt3 = 0
    while True:
        before = lines[index].strip()
        op = lines[index + 1].strip()
        after = lines[index + 2].strip()

        if 'Before:' not in before:
            break

        before_state = eval(before.split('Before: ')[1])
        instruction = Instruction._make(list(map(int, op.split())))
        after_state = eval(after.split('After:  ')[1])

        count = 0
        for fop in ops:
            if fop(getattr(instruction, 'A'), getattr(instruction, 'B'), getattr(instruction, 'C'), before_state) == after_state:
                count += 1

        if count >= 3:
            gt3 += 1
                
        index += 4
    print(gt3)
