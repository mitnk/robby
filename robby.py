import itertools
import logging
import random
import time

SIZE = 10
NUMBER_ROBBY = 200
NUMBER_WALK = 100

# 0 for empty
# 1 for can
# 2 for wall
def get_situations():
    situations = [''.join(x) for x in itertools.product('012', repeat=5)]
    result = {}
    for i in xrange(len(situations)):
        result[situations[i]] = i
    return result

SITUATIONS = get_situations()


def get_index_random_base():
    IRB = []
    TOP_NUMBER = 20
    total_number = 100
    for i in xrange(TOP_NUMBER):
        IRB.extend([i] * (TOP_NUMBER - i))
    for i in xrange(TOP_NUMBER, total_number):
        IRB.append(i)
    return IRB

INDEXES_RANDOM_BASE = get_index_random_base()

# now 2.09 seconds for 10000 times
def get_random_squares():
    squares = []
    for i in xrange(SIZE):
        s = []
        for j in xrange(SIZE):
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
    index = SITUATIONS[situation]
    action = robby[index]

    # pick up can
    if action == '5':
        if square[x][y] == 1:
            score = 10
            square[x][y] = 0
        else:
            score = -1
        return score + walk(square, robby, x, y, steps - 1)

    # stay still
    if action == '0':
        return 0

    # go a random direction
    if action == '6':
        action = random.sample('1234', 1)[0]

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
        _x = x - 1
        _y = y
    else:
        raise "How could you come here! action: %s" % action

    score = 0
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
    for i in xrange(243):
        m += str(random.randint(0, 6))
    return m


def get_state(square, x, y):
    if hit_wall(x, y):
        return '2' # wall
    else:
        return str(square[x][y]) # empty or can


def print_squares(squares):
    for y in xrange(SIZE):
        for x in xrange(SIZE):
            print squares[x][y],
        print ''

def get_new_robby(robbys, variation=4):
    idx_a = random.choice(INDEXES_RANDOM_BASE)
    parent_a = robbys[idx_a]['name']

    idx_b = random.choice(INDEXES_RANDOM_BASE)
    while idx_b == idx_a:
        idx_b = random.choice(INDEXES_RANDOM_BASE)
    parent_b = robbys[idx_b]['name']

    mid = random.randint(80, 160)
    robby1 = parent_a[:mid] + parent_b[mid:]
    robby2 = parent_b[:mid] + parent_a[mid:]
    vari = random.randint(1, 1000)
    if vari <= variation * 10:
        number = random.randint(1, 4)
        for i in xrange(number):
            idx = random.randint(1, 241)
            rand_action = random.randint(0, 6)
            robby1 = robby1[:idx] + str(rand_action) + robby1[idx + 1:]
    vari = random.randint(1, 1000)
    if vari >= 1000 - variation * 10:
        number = random.randint(1, 4)
        for i in xrange(number):
            idx = random.randint(1, 241)
            rand_action = random.randint(0, 6)
            robby2 = robby2[:idx] + str(rand_action) + robby2[idx + 1:]
    return robby1, robby2

def go_evolution(generations=1000):
    robbys = []
    for i in xrange(NUMBER_ROBBY):
        robby = {'name': get_random_robby(), 'score': 0 }
        robbys.append(robby)

    for j in xrange(generations):
        sum_scores = 0
        gene_best = -1000000
        for robby in robbys:
            scores = 0
            for i in xrange(NUMBER_WALK):
                squares = get_random_squares()
                scores += walk(squares, robby['name'])
                time.sleep(0.001)
            avg_score = scores / (NUMBER_WALK * 1.0)
            robby['score'] = avg_score
            sum_scores += avg_score
            if gene_best < avg_score:
                gene_best = avg_score

        robbys.sort(key=lambda x: x['score'], reverse=True)
        robbys = robbys[:100]
        AVG = sum_scores / (NUMBER_ROBBY * 1.0)
        logging.info("[%d, %.2f] AVG: %.2f" % (j, gene_best, AVG))
        new_robbys = []
        for i in xrange(100):
            robby1, robby2 = get_new_robby(robbys)
            robby1 = {'name': robby1, 'score': 0}
            robby2 = {'name': robby2, 'score': 0}
            new_robbys.append(robby1)
            new_robbys.append(robby2)
        robbys = new_robbys
        logging.info('=== %s' % robbys)

if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-f", "--logfile", dest="logfile",
        help="Save output into a file")
    (options, args) = parser.parse_args()
    logging.basicConfig(filename=options.logfile, level=logging.INFO,
        format="[%(asctime)s][%(levelname)s] %(message)s")
    go_evolution(3)
