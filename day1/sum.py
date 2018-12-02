with open('input.txt', 'r') as f:
    input_freq = [int(line) for line in f.readlines()]

    # Part 1:
    print("Part 1: " + str(sum(input_freq)))

    # Part 2:
    cur_sum = 0
    seen = set()
    index = 0
    while not cur_sum in seen:
        seen.add(cur_sum)
        cur_sum += input_freq[index]
        index = (index + 1) % len(input_freq)
    print("Part 2: " + str(cur_sum))
