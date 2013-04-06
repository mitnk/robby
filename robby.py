import itertools
import random

SIZE = 10

# 0 for empty
# 1 for can
# 2 for wall
def get_situations():
    return [''.join(x) for x in itertools.product('012', repeat=5)]

SITUATIONS = get_situations()


def get_index_random_base():
    IRB = []
    TOP_NUMBER = 20
    total_number = 100
    for i in range(TOP_NUMBER):
        IRB.extend([i] * (TOP_NUMBER - i))
    for i in range(TOP_NUMBER, total_number):
        IRB.append(i)
    return IRB

INDEXES_RANDOM_BASE = get_index_random_base()

# now 2.09 seconds for 10000 times
def get_random_squares():
    squares = []
    for i in range(SIZE):
        s = []
        for j in range(SIZE):
            a = random.randint(1, 100)
            if a >= 51:
                s.append(1)
            else:
                s.append(0)
        squares.append(s)
    return squares


def hit_wall(x, y):
    return x < 0 or y < 0 or x >= SIZE or y >= SIZE


# situation location order:
# up right down left self
def walk(square, robby, x=0, y=0, steps=200):
    if steps <= 0:
        return 0

    situation = ''
    situation += get_state(square, x, y - 1) # up
    situation += get_state(square, x + 1, y) # right
    situation += get_state(square, x, y + 1) # down
    situation += get_state(square, x - 1, y) # left
    situation += get_state(square, x, y) # self
    index = SITUATIONS.index(situation)
    action = robby[index]
    score = 0

    if action == '5': # pick can
        if square[x][y] == 1:
            score = 10
            square[x][y] = 0
        else:
            score = -1
    elif action == '0': # stay still
        score = 0
        steps = 0

    elif action == '6': # go a random direction
        action = random.sample('1234', 1)[0]

    _x = x
    _y = y
    if action == '1': # go up
        _x = x
        _y = y - 1
    elif action == '2': # go right
        _x = x + 1
        _y = y
    elif action == '3': # go down
        _x = x
        _y = y + 1
    elif action == '4': # go left
        _x = _x - 1
        _y = y

    if hit_wall(_x, _y):
        score = -5
        _x = x
        _y = y
    return score + walk(square, robby, _x, _y, steps - 1)


# 0 for stay still
# 1 for go up
# 2 for go right
# 3 for go down
# 4 for go left
# 5 for pick
# 6 for go random one of (up / right / down / left)
def get_random_robby():
    m = ""
    for i in range(243):
        m += str(random.randint(0, 6))
    return m


def get_state(square, x, y):
    if hit_wall(x, y):
        return '2' # wall
    else:
        return str(square[x][y]) # empty or can


def print_squares(squares):
    for y in range(SIZE):
        for x in range(SIZE):
            print squares[x][y],
        print ''

def get_new_robby(robbys, avg_score):
    idx_a = random.sample(INDEXES_RANDOM_BASE, 1)[0]
    parent_a = robbys[idx_a]['name']

    idx_b = random.sample(INDEXES_RANDOM_BASE, 1)[0]
    while idx_b == idx_a:
        idx_b = random.sample(INDEXES_RANDOM_BASE, 1)[0]
    parent_b = robbys[idx_b]['name']

    index = random.randint(1, 241)
    robby1 = parent_a[:index] + parent_b[index:]
    robby2 = parent_b[:index] + parent_a[index:]
    vari = random.randint(1, 100)
    if vari < 5:
        number = random.randint(1, 4)
        for i in range(number):
            idx = random.randint(1, 241)
            rand_action = random.randint(0, 6)
            robby1 = robby1[:idx] + str(rand_action) + robby1[idx + 1:]
    vari = random.randint(1, 100)
    if vari > 94:
        number = random.randint(1, 4)
        for i in range(number):
            idx = random.randint(1, 241)
            rand_action = random.randint(0, 6)
            robby2 = robby2[:idx] + str(rand_action) + robby2[idx + 1:]
    return robby1, robby2



def main():
    import time

    #print_squares(squares)
    robbys = []
    for i in range(200):
        robby = {'name': get_random_robby(), 'score': -1000000000}
        robbys.append(robby)

    for j in range(1000):
        an_scores = 0
        count = 0
        BEST = -1000000
        for robby in robbys:
            scores = 0
            for i in range(100):
                squares = get_random_squares()
                scores += walk(squares, robby['name'])
                time.sleep(0.001)
            count += 1
            avg_score = scores / 100.0
            robby['score'] = avg_score
            an_scores += avg_score
            if BEST < avg_score:
                BEST = avg_score

        robbys.sort(key=lambda x: x['score'], reverse=True)
        robbys = robbys[:100]
        AVG = an_scores / 200.0
        print "[%d, %.2f] AVG: %.2f" % (j, BEST, AVG)
        new_robbys = []
        for i in range(100):
            robby1, robby2 = get_new_robby(robbys, AVG)
            robby1 = {'name': robby1, 'score': 0}
            robby2 = {'name': robby2, 'score': 0}
            new_robbys.append(robby1)
            new_robbys.append(robby2)
        robbys = new_robbys
        break

if __name__ == '__main__':
    #main()
    for i in range(10000):
        get_random_squares()
