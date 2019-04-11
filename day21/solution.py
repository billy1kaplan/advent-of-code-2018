from collections import namedtuple, defaultdict

add = lambda x, y: x + y
prod = lambda x, y: x * y
band = lambda x, y: x & y
bor = lambda x, y: x | y
gt = lambda x, y: 1 if x > y else 0
eq = lambda x, y: 1 if x == y else 0

def rrfunc(A, B, C, init, bin_op):
    result = init[:]
    result[C] = bin_op(init[A], init[B])
    return result

def irfunc(A, B, C, init, bin_op):
    result = init[:]
    result[C] = bin_op(A, init[B])
    return result

def rifunc(A, B, C, init, bin_op):
    result = init[:]
    result[C] = bin_op(init[A], B)
    return result

def iifunc(A, B, C, init, bin_op):
    result = init[:]
    result[C] = bin_op(A, B)
    return result

def addr(A, B, C, init):
    return rrfunc(A, B, C, init, add)

def addi(A, B, C, init):
    return rifunc(A, B, C, init, add)

def mulr(A, B, C, init):
    return rrfunc(A, B, C, init, prod)

def muli(A, B, C, init):
    return rifunc(A, B, C, init, prod)

def banr(A, B, C, init):
    return rrfunc(A, B, C, init, band)

def bani(A, B, C, init):
    return rifunc(A, B, C, init, band)

def borr(A, B, C, init):
    return rrfunc(A, B, C, init, bor)

def bori(A, B, C, init):
    return rifunc(A, B, C, init, bor)

def setr(A, B, C, init):
    return rifunc(A, B, C, init, lambda a, b: a)

def seti(A, B, C, init):
    return iifunc(A, B, C, init, lambda a, b: a)

def gtir(A, B, C, init):
    return irfunc(A, B, C, init, gt)

def gtri(A, B, C, init):
    return rifunc(A, B, C, init, gt)

def gtrr(A, B, C, init):
    return rrfunc(A, B, C, init, gt)

def eqir(A, B, C, init):
    return irfunc(A, B, C, init, eq)

def eqri(A, B, C, init):
    return rifunc(A, B, C, init, eq)

def eqrr(A, B, C, init):
    return rrfunc(A, B, C, init, eq)

ops = { 'addr' :  addr,
        'addi' :  addi,
        'mulr' :  mulr,
        'muli' :  muli,
        'banr' :  banr,
        'bani' :  bani,
        'borr' :  borr,
        'bori' :  bori,
        'setr' :  setr,
        'seti' :  seti,
        'gtir' :  gtir,
        'gtri' :  gtri,
        'gtrr' :  gtrr,
        'eqir' :  eqir,
        'eqri' :  eqri,
        'eqrr' :  eqrr }

def to_binary(n):
    cur = n
    res = []
    while cur > 0:
        res.append(cur & 1)
        cur >>= 1
    if len(res) == 0:
        return '0'
    return ''.join([str(ch) for ch in res[::-1]])

def regs2bin(regs): 
    return [to_binary(n) for n in regs]

with open('input.txt', 'r') as f:
    registers = [0 for _ in range(6)]
    registers[0] = 5745417
    ip_reg = int(''.join([ch for ch in f.readline() if ch.isnumeric()]))
    instructions = [line.split() for line in f.readlines()]

    while registers[ip_reg] >= 0 and registers[ip_reg] < len(instructions):
        cur_inst = instructions[registers[ip_reg]]
        op, one, two, three = cur_inst[:1] + list(map(int, cur_inst[1:]))
        prev_registers = registers
        registers = ops[op](one, two, three, registers)
        print(f'ip={prev_registers[ip_reg]} {regs2bin(prev_registers)} {op} {one} {two} {three} {regs2bin(registers)}')
        registers[ip_reg] += 1

    print(registers[0])
