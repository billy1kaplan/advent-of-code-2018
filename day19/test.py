from math import sqrt, ceil
def factors(n):
    res = []
    for i in range(1, 1 + int(ceil(sqrt(n)))):
        if n % i == 0:
            if n // i == i:
                res.append(i)
            else:
                res.extend([i, n // i])
    return res

f = factors(900)
print(f, sum(f))

s = sorted(f)
print(s)
s_part = [sum(s[:i]) for i in range(len(s) + 1)]
print(s_part)
