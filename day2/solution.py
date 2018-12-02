from collections import defaultdict

with open('input.txt', 'r') as f:
    lines = f.readlines()

    #Part 1
    def count(word, n):
        counts = defaultdict(int)
        for ch in word:
            counts[ch] += 1
        return any(filter(lambda x: x == n, counts.values()))

    count2 = 0
    count3 = 0
    for line in lines:
        if count(line, 2):
            count2 += 1
        if count(line, 3):
            count3 += 1
    print(count2 * count3)

    #Part 2
    def difference(word1, word2):
        count = 0
        for ch1, ch2 in zip(word1, word2):
            if not ch1 == ch2:
                count += 1
        return count

    def make_same(word1, word2):
        res = ""
        for ch1, ch2 in zip(word1, word2):
            if ch1 == ch2:
                res += ch1
        return res

    for line in lines:
        for other_line in lines:
            if difference(line, other_line) == 1:
                print(make_same(line, other_line))
