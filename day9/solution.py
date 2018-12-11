from collections import deque

n_players = 459
last_marble = 71790 * 100

#n_players = 9
#last_marble = 25

marbles = deque([0])
scores = { player : 0 for player in range(n_players) }
cur_player = 0
for marble_score in range(1, last_marble + 1):
    if marble_score % 23 == 0:
        marbles.rotate(7)
        scores[cur_player] += marble_score + marbles.popleft()
    else:
        marbles.rotate(-2)
        marbles.appendleft(marble_score)

    cur_player = (cur_player + 1) % n_players

print("Best score", max(scores.values()))
