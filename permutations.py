cards = [1, 2, 3]

def permutate(values):
    result = []
    def internal(vals, acc):
        if vals == []:
            result.append(acc)
        else:
            for i in range(len(vals)):
                internal(vals[:i] + vals[i+1:], acc + [vals[i]])

    internal(values, [])
    return result
print(permutate(cards))
