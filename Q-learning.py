import numpy as np
from random import randint
import random

"""

s = state = état de l'agent

spt = state position au temps t
sot = state orientation au temps t
self.oreint = : 0 = right, 1 = up, 2 = left, 3 = down

at = action au temps t
Action: 0 = TURN_LEFT, 1 = TURN_RIGH, 2 = FORWARD, 3 = FORWARD_RIGHT, 4 = FORWARD_LEFT

sptp1 = state position au temps t+1
sotp1 = state orientation au temps t+1

atp1 = action au temps t+1

r = récompense 

"""

bonus = []
checkpoint_1 = 0
checkpoint_2 = 0
checkpoint_3 = 0
checkpoint_4 = 0
score = 0


class EnvGrid(object):
    def __init__(self):
        super(EnvGrid, self).__init__()

        self.grid = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [-1,  0,  0,  0,  0,  2,  0,  0,  0, -1],
                     [-1,  0,  0,  0,  0,  2,  0,  0,  0, -1],
                     [-1,  0,  0,  0,  0, -1, -1,  0,  0, -1],
                     [-1,  0,  0, -1, -1, -1, -1,  2,  2, -1],
                     [-1,  2,  2, -1, -1, -1, -1,  0,  0, -1],
                     [-1,  0,  0, -1, -1,  0,  0,  0,  0, -1],
                     [-1,  0,  0,  0,  2,  0,  0,  0,  0, -1],
                     [-1,  0,  0,  0,  2,  0,  0,  0,  0, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

        self.y = 2
        self.x = 3
        self.orient = 0

        self.actions = [
            0,  # TURN_LEFT
            1,  # TURN_LEFT
            2,  # FORWARD_RIGHT
            3,  # FORWARD
            4,  # FORWARD_LEFT
        ]

    def reset(self):
        global checkpoint_1, checkpoint_2, checkpoint_3, checkpoint_4

        self.y = 2
        self.x = 3
        self.orient = 0
        checkpoint_1 = 20
        checkpoint_2 = 20
        checkpoint_3 = 20
        checkpoint_4 = 20
        return(self.y*10+self.x+1), self.orient

    def step(self, action):
        """
            Action: 0 = TURN_LEFT, 1 = TURN_RIGH, 2 = FORWARD, 3 = FORWARD_RIGHT, 4 = FORWARD_LEFT
            Orientation: 0 = Right, 1 = Up, 2 = Left, 3 = Down
        """

        if self.actions[action] == 0:
            # print("TURN_LEFT")
            if self.orient == 2:
                self.orient = 3
            elif self.orient == 3:
                self.orient = 0
            elif self.orient == 0:
                self.orient = 1
            elif self.orient == 1:
                self.orient = 2

        elif self.actions[action] == 1:
            # print("TURN_RIGHT")
            if self.orient == 2:
                self.orient = 1
            elif self.orient == 1:
                self.orient = 0
            elif self.orient == 0:
                self.orient = 3
            elif self.orient == 3:
                self.orient = 2

        elif self.actions[action] == 2:
            # print("FORWARD_RIGHT")
            if self.orient == 2:
                self.y += -1
                self.x += -1
            elif self.orient == 0:
                self.y += 1
                self.x += 1
            elif self.orient == 1:
                self.y += -1
                self.x += 1
            elif self.orient == 3:
                self.y += 1
                self.x += -1

        elif self.actions[action] == 3:
            # print("FORWARD")
            if self.orient == 2:
                self.x += -1
            elif self.orient == 0:
                self.x += 1
            elif self.orient == 1:
                self.y += -1
            elif self.orient == 3:
                self.y += 1

        elif self.actions[action] == 4:
            # print("FORWARD_LEFT")
            if self.orient == 2:
                self.y += 1
                self.x += -1
            elif self.orient == 0:
                self.y += -1
                self.x += 1
            elif self.orient == 1:
                self.y += -1
                self.x += -1
            elif self.orient == 3:
                self.y += 1
                self.x += 1

        return (self.y*10+self.x+1), self.orient, self.grid[self.y][self.x]  # return sptp1, sotp1, r

    def reward(self):
        global bonus, checkpoint_1, checkpoint_2, checkpoint_3, checkpoint_4

        checkpoint_1 += 1
        checkpoint_2 += 1
        checkpoint_3 += 1
        checkpoint_4 += 1

        for _ in range(2):

            if self.grid[self.y][self.x] == 2:
                bonus.append(self.x)
                self.grid[self.y][self.x] = 0

            if 5 in bonus:
                self.grid[1][5] = 0
                self.grid[2][5] = 0
            else:
                self.grid[1][5] = 2
                self.grid[2][5] = 2
                checkpoint_1 = 0
            if checkpoint_1 >= 18:
                checkpoint_1 = 0
                bonus.remove(5)

            if 7 in bonus or 8 in bonus:
                self.grid[4][7] = 0
                self.grid[4][8] = 0
            else:
                self.grid[4][7] = 2
                self.grid[4][8] = 2
                checkpoint_2 = 0

            if checkpoint_2 >= 18:
                checkpoint_2 = 0
                if 7 in bonus:
                    bonus.remove(7)
                else:
                    bonus.remove(8)

            if 4 in bonus:
                self.grid[7][4] = 0
                self.grid[8][4] = 0
            else:
                self.grid[7][4] = 2
                self.grid[8][4] = 2
                checkpoint_3 = 0

            if checkpoint_3 >= 18:
                checkpoint_3 = 0
                bonus.remove(4)

            if 2 in bonus or 1 in bonus:
                self.grid[5][1] = 0
                self.grid[5][2] = 0
            else:
                self.grid[5][1] = 2
                self.grid[5][2] = 2
                checkpoint_4 = 0

            if checkpoint_4 >= 18:
                checkpoint_4 = 0
                if 2 in bonus:
                    bonus.remove(2)
                else:
                    bonus.remove(1)

    def show(self):

        y = 0
        for line in self.grid:
            x = 0
            for pt in line:
                if self.orient == 2:
                    print("{}\t".format(pt if y != self.y or x != self.x else "◄"), end="")
                elif self.orient == 0:
                    print("{}\t".format(pt if y != self.y or x != self.x else "►"), end="")
                elif self.orient == 1:
                    print("{}\t".format(pt if y != self.y or x != self.x else "▲"), end="")
                elif self.orient == 3:
                    print("{}\t".format(pt if y != self.y or x != self.x else "▼"), end="")
                x += 1
            y += 1
            print("")
        print("---------------------")

    def is_finished(self):
        return self.grid[self.y][self.x] == -1


def take_action(spt, sot, Q, eps):

    if random.uniform(0, 1) < eps:
        action = randint(0, 4)
    else:
        if np.argmax(Q[spt][sot]) == 0:
            action = randint(0, 4)
        else:
            action = np.argmax(Q[spt][sot])
    return action


if __name__ == '__main__':
    env = EnvGrid()

    rep = 10000
    epsilon = 1

    Q = [  # 100 listes de 4 listes de 5 valeurs : 100 positions, 4 orientations, 5 actions
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    ]

    for _ in range(rep):
        spt, sot = env.reset()

        if (_ + 1) % 100 == 0 or _ > rep-2:
            print("{} sur {}".format(_ + 1, rep))
            print("{} = {}".format("Epsilon", epsilon))

        if _ > rep-2:
            print("reset")
            env.show()

        epsilon = max(epsilon * (1 - 1 / (rep / 5)), 0.01)
        # Décroissant logarithmiquement, plus lent mais meilleur score
        # epsilon = max(epsilon - (1 / (rep/1.1)), 0.01)
        # Décroissant linéairement, plus rapide mais légèrement moins bon score
        # Rapport score/temps meilleurs avec une décroissance linéaire

        while not env.is_finished():
            at = take_action(spt, sot, Q, epsilon)

            sptp1, sotp1, r = env.step(at)

            atp1 = take_action(sptp1, sotp1, Q, 0.0)
            Q[spt][sot][at] = Q[spt][sot][at] + 0.1*(r + 0.9*Q[sptp1][sotp1][atp1] - Q[spt][sot][at])

            env.reward()
            if _ > rep-101:
                score += r
                if _ > rep-2:
                    env.show()
                    # epsilon = 0

            spt = sptp1
            sot = sotp1

    for s in range(11, 91):
        print(s, Q[s])

    print(score/100)
