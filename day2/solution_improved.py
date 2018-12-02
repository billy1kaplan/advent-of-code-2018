from collections import defaultdict

with open('input.txt', 'r') as f:
    lines = f.readlines()

    # Part 1
    # defaultdict<char, int> -> boolean
    def count(frequencies, n):
        return len(list(filter(lambda x: x == n, counts.values()))) > 0

    count2 = 0
    count3 = 0
    for line in lines:
        counts = defaultdict(int)
        for ch in line:
            counts[ch] += 1

        if count(counts, 2): count2 += 1 
        if count(counts, 3): count3 += 1 
    print(count2 * count3)

    # Part 2
    def common(word1, word2):
        return ''.join([ch1 for ch1, ch2 in zip(word1, word2) if ch1 == ch2])

    def find_one_off():
        for line in lines:
            for other_line in lines:
                common_chars = common(line, other_line)
                if len(common_chars) == len(line) - 1:
                    print(common_chars)
                    return None
    find_one_off()
