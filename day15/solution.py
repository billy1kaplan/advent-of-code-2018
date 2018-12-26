from collections import deque

class Battle:
    def __init__(self, battlefield):
        self.battlefield = battlefield
        self.dead_elf = False

    def _setup(self):
        for row in self.battlefield:
            for pos in row:
                pos.occupier.register(self)

    def notify(self):
        self.dead_elf = True

    def detect_heartbeat(self):
        elf_hb, goblin_hb = False, False
        for row in self.battlefield:
            for actor in row:
                e, g = actor.occupier.heartbeat()
                elf_hb = elf_hb or e
                goblin_hb = goblin_hb or g
        return (elf_hb, goblin_hb)

    def simulate(self):
        self._setup()
        elf_heartbeat, goblin_heartbeat = True, True
        round_number = 0
        print(self)
        print()

        while elf_heartbeat and goblin_heartbeat:
            round_number += 1
            elf_heartbeat, goblin_heartbeat = False, False

            # Perform all actions
            for row in self.battlefield:
                for actor in row:
                    e, g = actor.act(round_number)
                    if self.dead_elf:
                        raise Exception('Mission Failed')
                    if e or g:
                        elf_heartbeat, goblin_heartbeat = self.detect_heartbeat()
                        if not elf_heartbeat or not goblin_heartbeat:
                            return self.compute_outcome(round_number - 1)

            # Detect heartbeats
            elf_heartbeat, goblin_heartbeat = self.detect_heartbeat()

            # Print Debug Info
            #print(round_number)
            #print(elf_heartbeat, goblin_heartbeat)
            #print(self)
            #for row in self.battlefield:
            #    for pos in row:
            #        if pos.occupier.hitpoints > 0:
            #            print(str(pos.occupier), str(pos.occupier.hitpoints))

        return self.compute_outcome(round_number)

    def compute_outcome(self, round_number):
        # Print Final Result
        hp_sum = sum([pos.occupier.hitpoints for row in self.battlefield for pos in row])
        last_full_round = round_number
        print(f'Summary: Final Round = {last_full_round}, HP Sum = {hp_sum}')
        return last_full_round * hp_sum

    def __str__(self):
        return '\n'.join([''.join([str(pos.occupier) for pos in row]) for row in self.battlefield])

class Position:
    def __init__(self, position):
        self.position = position
        self.left, self.right, self.up, self.down = None, None, None, None
        self.occupier = None

    def act(self, round_number):
        return self.occupier.act(self, round_number)

    def move_to(self, other_position):
        other_position.occupier = self.occupier
        self.occupier = OpenSpace()
        #print('MOVE', str(self), 'TO', str(other_position))
        return other_position

    def receive_hit(self, dmg):
        self.occupier = self.occupier.receive_hit(dmg)

    def find_enemy(self, warrior):
        positions = [self.up, self.left, self.right, self.down]
        visited = set(positions)
        for position in positions:
            if warrior.is_enemy(position.occupier): 
                return ([], position)

        visited_neighbors = set(positions)
        visit_queue = deque(list(map(lambda pos: ([], pos), positions)))

        while len(visit_queue) > 0:
            path, first = visit_queue[0]

            if warrior.is_enemy(first.occupier):
                candidates = [(cur_path, pos) for cur_path, pos in visit_queue if len(path) == len(cur_path) and warrior.is_enemy(pos.occupier)]
                read_order = sorted(candidates, key = lambda candidate: candidate[0][-1].position)
                return read_order[0]
            else:
                visit_queue.popleft()
                for neighbor in first.neighbors():
                    if neighbor not in visited: 
                        visited.add(neighbor)
                        visit_queue.append((path + [first], neighbor))

        return False

    def attack(self, warrior):
        positions = [self.up, self.left, self.right, self.down]
        enemies = [other for other in positions if warrior.is_enemy(other.occupier)]
        weakest = sorted(enemies, key=lambda pos: pos.occupier.hitpoints)
        if len(weakest) > 0:
            warrior.attack(weakest[0])

    def neighbors(self):
        return self.occupier.visit([self.up, self.left, self.right, self.down])

    def __str__(self):
        return str(self.occupier) + ' @ ' + str(self.position)

class Barrier:
    def __init__(self):
        self.hitpoints = 0

    def heartbeat(self):
        return (False, False)

    def register(self, listener):
        pass

    def visit(self, neighbors):
        return []

    def act(self, position, round_number):
        return (False, False)

    def is_enemy(self, requester):
        return False

    def __str__(self):
        return '#'

class OpenSpace:
    def __init__(self):
        self.hitpoints = 0

    def heartbeat(self):
        return (False, False)

    def register(self, listener):
        pass

    def visit(self, neighbors):
        return neighbors

    def act(self, position, round_number):
        return (False, False)

    def is_enemy(self, requester):
        return False

    def __str__(self):
        return '.'

class Warrior:
    def __init__(self, hitpoints=200, attack_power=3, round_number=0):
        self.hitpoints = hitpoints
        self.attack_power = attack_power
        self.round_number = round_number

    def act(self, position, round_number):
        if round_number > self.round_number:
            self.round_number += 1
            self._act(position)
            return self.heartbeat()
        return (False, False)

    def _act(self, position):
        path_to_nearest = position.find_enemy(self)
        attack_position = position
        if path_to_nearest:
            path, other_position = path_to_nearest

            if path != []:
                attack_position = position.move_to(path[0])
        attack_position.attack(self)

    def attack(self, other_position):
        other_position.receive_hit(self.attack_power)

    def receive_hit(self, dmg):
        self.hitpoints -= dmg

        if self.hitpoints <= 0:
            self.notify_all()
            return OpenSpace()
        else:
            return self

    def visit(self, neighbors):
        return []

class Elf(Warrior):
    def __init__(self, attack_power=3):
        self.listener = None
        self.attack_power = attack_power
        super(Elf, self).__init__(attack_power=attack_power)

    def __str__(self):
        return 'E'

    def register(self, listener):
        self.listener = listener

    def heartbeat(self):
        return (True, False)

    def notify_all(self):
        self.listener.notify()

    def is_enemy(self, requester):
        return isinstance(requester, Goblin)

class Goblin(Warrior):
    def __str__(self):
        return 'G'

    def register(self, listener):
        pass

    def notify_all(self):
        pass

    def heartbeat(self):
        return (False, True)

    def is_enemy(self, requester):
        return isinstance(requester, Elf)

def simulate_with_weapon_power(power):
    with open('input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        grid = [[Position((row, col)) for col in range(len(lines[row]))] for row in range(len(lines))]

        for row in range(1, len(lines) - 1):
            for col in range(1, len(lines[row]) - 1):
                position = grid[row][col] 
                position.left = grid[row][col-1]
                position.right = grid[row][col+1]
                position.up = grid[row-1][col]
                position.down = grid[row+1][col]

        for row in range(len(lines)):
            for col in range(len(lines[row])):
                item = lines[row][col]
                position = grid[row][col]
                if item == 'G':
                    position.occupier = Goblin()
                elif item == 'E':
                    position.occupier = Elf(attack_power=power)
                elif item == '.':
                    position.occupier = OpenSpace()
                elif item == '#':
                    position.occupier = Barrier()

        battle = Battle(grid)
        print(battle.simulate())

def binary_search_weapon_power():
    low = 4
    high = 200

    while low < high:
        print(low, high)
        mid = (low + high) // 2
        try:
            simulate_with_weapon_power(mid)
            print('Succeeded', mid)
            high = mid
        except Exception:
            print('Failed', mid)
            low = mid + 1
    print(f'Power needed: {low}, {high}')
binary_search_weapon_power()
