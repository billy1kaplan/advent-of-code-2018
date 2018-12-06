import re

with open('input.txt', 'r') as f:
    lines = sorted(f.readlines())

    extract_numbers = re.compile(r'\d+')
    # DATE id
    # DATE F
    # DATE W
    def extract(line):
        nums = re.findall(extract_numbers, line)
        nums = list(map(int, nums))
        if "falls asleep" in line:
            nums.append('F')
        elif "wakes up" in line:
            nums.append('W')
        return nums

    def elapsed_time(time1, time2):
        year1, month1, day1, hour1, minute1, _ = time1
        year2, month2, day2, hour2, minute2, _ = time2
        return minute2 - minute1

    guards = {}
    prev_time = extract(lines[0])
    cur_guard = prev_time[-1]
    is_awake = True
    for line in lines[1:]:
        cur_time = extract(line)

        action = cur_time[-1]
        if action == 'F':
            is_awake = False
        elif action == 'W':
            is_awake = True

            if cur_guard not in guards:
                guards[cur_guard] = 0
            guards[cur_guard] += elapsed_time(prev_time, cur_time)
        else:
            cur_guard = action
            is_awake = True

        prev_time = cur_time

    sleepiest = sorted(guards.items(), key = lambda item: item[1])[-1][0]
    asleep = [0] * 60

    prev_time = extract(lines[0])
    cur_guard = prev_time[-1]
    is_awake = True
    for line in lines[1:]:
        cur_time = extract(line)

        action = cur_time[-1]
        if action == 'F':
            is_awake = False
        elif action == 'W':
            is_awake = True

            if cur_guard == sleepiest:
                for minute in range(prev_time[4], cur_time[4]):
                    asleep[minute] += 1
        else:
            cur_guard = action
            is_awake = True

        prev_time = cur_time

    most = max(asleep)

    for  minute, count in enumerate(asleep):
        if count == most:
            print(minute * sleepiest)
            break

    # Part 2
    sleepmins = {}
    prev_time = extract(lines[0])
    cur_guard = prev_time[-1]
    is_awake = True
    for line in lines[1:]:
        cur_time = extract(line)

        action = cur_time[-1]
        if action == 'F':
            is_awake = False
        elif action == 'W':
            is_awake = True


            if not cur_guard in sleepmins:
                sleepmins[cur_guard] = [0] * 60
            for minute in range(prev_time[4], cur_time[4]):
                sleepmins[cur_guard][minute] += 1
        else:
            cur_guard = action
            is_awake = True

        prev_time = cur_time

    sleepy_guard, most, sleepiest_min = None, 0, 0
    for guard, minutes in sleepmins.items():
        for m, count in enumerate(minutes):
            if count > most:
                most = count
                sleepy_guard = guard
                sleepiest_min = m

    print(sleepy_guard, sleepiest_min, sleepy_guard * sleepiest_min)
