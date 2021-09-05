TAB = [[100,   7,  12,  15,  10, 100,   9,  10,  12,  14,  15, 100, 100],
       [ 10, 999,   4,   6, 100, 100,   2,   6,   8,  10,   8,   2,   4],
       [100,   5, 999,   3, 100, 100,   4,   3,   5,   7, 100,   5,   6],
       [100, 100,   5, 999,   5, 100,   4,   4,   5,   8, 100,   7,   5],
       [100, 100, 100,   5, 999,   3, 100,   8,   7,   8, 100, 100, 100],
       [100, 100, 100, 100,   4, 999,   5,   5,   7, 100, 100, 100, 100],
       [100, 100,   4,   2, 100,   5, 999,   2,   4,   6, 100,   3,   4],
       [  8, 100, 100,   5, 100, 100,   3, 999,   3,   5, 100,   5,   8],
       [  6, 100, 100, 100, 100, 100, 100, 100, 100,   2, 100, 100, 100],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100,   4, 100, 100],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,   6, 100],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,   4],
       [  7, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]]

LOWEST_KNOWN_SCORES = [145] * 10
NUM_CHECKPOINTS = 13


def computeScore(path, score):
    global LOWEST_KNOWN_SCORES
    if len(path) == NUM_CHECKPOINTS:
        score += TAB[path[-1]][0]
        if score < LOWEST_KNOWN_SCORES[-1]:
            LOWEST_KNOWN_SCORES += [score]
            LOWEST_KNOWN_SCORES.sort()
            LOWEST_KNOWN_SCORES = LOWEST_KNOWN_SCORES[:-1]
            print(f"New score : {score} with path {path}")
    elif score < LOWEST_KNOWN_SCORES[-1]:
        for i in range(13):
            if i not in path:
                computeScore(path + [i], score + TAB[path[-1]][i])


computeScore([0], 0)
print(LOWEST_KNOWN_SCORES)
