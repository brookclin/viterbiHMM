import math
f = open('hmm-data.txt')
lines = f.readlines()
f.close()
grid = []
obs = []
V = []
path = {}
for i in range(2, 12):
    grid.append(map(int, lines[i].split()))
for i in range(24, 35):
    obs.append(map(float, lines[i].split()))


def possible_states(a, b):
    state_list = []
    if a - 1 >= 0 and grid[a - 1][b] == 1:
        state_list.append((a - 1, b))
    if a + 1 <= 9 and grid[a + 1][b] == 1:
        state_list.append((a + 1, b))
    if b - 1 >= 0 and grid[a][b - 1] == 1:
        state_list.append((a, b - 1))
    if b + 1 <= 9 and grid[a][b + 1] == 1:
        state_list.append((a, b + 1))
    return state_list


def in_obs_range(a, b, time):
    if grid[a][b] == 0:
        return False
    else:
        d1 = (a ** 2 + b ** 2) ** (1 / 2.0)
        d2 = (a ** 2 + (b - 9) ** 2) ** (1 / 2.0)
        d3 = ((a - 9) ** 2 + b ** 2) ** (1 / 2.0)
        d4 = ((a - 9) ** 2 + (b - 9) ** 2) ** (1 / 2.0)
        if 0.7 * d1 > obs[time][0] or obs[time][0] > 1.3 * d1:
            return False
        if 0.7 * d2 > obs[time][1] or obs[time][1] > 1.3 * d2:
            return False
        if 0.7 * d3 > obs[time][2] or obs[time][2] > 1.3 * d3:
            return False
        if 0.7 * d4 > obs[time][3] or obs[time][3] > 1.3 * d4:
            return False
        return True


def emit_p(a, b):
    d1 = (a ** 2 + b ** 2) ** (1 / 2.0)
    d2 = (a ** 2 + (b - 9) ** 2) ** (1 / 2.0)
    d3 = ((a - 9) ** 2 + b ** 2) ** (1 / 2.0)
    d4 = ((a - 9) ** 2 + (b - 9) ** 2) ** (1 / 2.0)
    prob1 = 1.0 / (math.floor(1.3 * d1 * 10) - math.ceil(0.7 * d1 * 10) + 1)
    prob2 = 1.0 / (math.floor(1.3 * d2 * 10) - math.ceil(0.7 * d2 * 10) + 1)
    prob3 = 1.0 / (math.floor(1.3 * d3 * 10) - math.ceil(0.7 * d3 * 10) + 1)
    prob4 = 1.0 / (math.floor(1.3 * d4 * 10) - math.ceil(0.7 * d4 * 10) + 1)
    return prob1 * prob2 * prob3 * prob4

# t == 0, initial first possible states
V.append({})
for i in range(0,10):
    for j in range(0,10):
        if not in_obs_range(i, j, 0):
            V[0][(i, j)] = 0
        else:
            V[0][(i, j)] = emit_p(i, j)
            path[(i, j)] = [(i, j)]


# run Viterbi for t > 0
for t in range(1, len(obs)):
    print "---------- t =", t, "----------"
    V.append({})
    newpath = {}

    for i in range(0, 10):
        for j in range(0, 10):
            if not in_obs_range(i, j, t):
                V[t][(i, j)] = 0
            else:
                states = possible_states(i, j)
                states = [state for state in states if V[t-1][state] != 0]
                if not states:
                    V[t][(i, j)] = 0
                else:
                    candidates = [(V[t-1][(i0, j0)] * (1.0/len(possible_states(i0, j0))) * emit_p(i, j), (i0, j0))
                                  for (i0, j0) in states]
                    (prob, state) = max(candidates)
                    candidates = [candidate[1] for candidate in candidates if candidate[0] == prob]
                    if len(candidates) > 1:
                        print "\t", "candidates of", (i, j)
                        print "\t", candidates
                        state = min(candidates)
                    print state, "->", (i, j), ",", prob
                    V[t][(i, j)] = prob
                    newpath[(i, j)] = path[state] + [(i, j)]

    path = newpath
    print "Possible path:"
    for key in path.keys():
        print key, path[key]

candidates = []
for i in range(0,10):
    for j in range(0,10):
        if V[len(obs)-1][(i, j)] != 0:
            candidates.append((V[len(obs)-1][(i, j)], (i, j)))
(prob, state) = max(candidates)
candidates = [candidate[1] for candidate in candidates if candidate[0] == prob]
if len(candidates) > 1:
    state = min(candidates)
print "---------- Final path ----------"
print path[state]

