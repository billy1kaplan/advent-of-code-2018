def generate():
    state, elf1, elf2 = [3, 7], 0, 1

    # Infinite Generator
    while True:
        recipe_sum = state[elf1] + state[elf2]
        dig1, dig2 = divmod(recipe_sum, 10)

        if dig1:
            state.append(dig1)
        state.append(dig2)

        elf1 = (elf1 + state[elf1] + 1) % len(state)
        elf2 = (elf2 + state[elf2] + 1) % len(state)
        yield state

def after_n(i, n):
    generator = generate()
    state = next(generator)
    while len(state) < i + n:
        state = next(generator)
    return state[i: i+n+1]

#print(''.join([str(i) for i in after_n(702831, 10)]))

# Part 2:
def recipes_before(n):
    generator = generate()
    state = next(generator)
    while n not in ''.join(list(map(str, state[-(len(n) + 1):]))):
        state = next(generator)
    return ''.join(list(map(str, state))).index(n)

print(recipes_before('702831'))
