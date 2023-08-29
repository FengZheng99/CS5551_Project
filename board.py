# Board class
class Board:

    # initiate
    def __init__(self, cord):
        self.cord = cord
        self.board = [0] * len(cord)
        self.player = 1
        self.placingMen = 0
        self.countMan = [9, 9]

    # change turn
    def change_turn(self):
        self.player *= -1

    # reset the board
    def reset(self):
        self.board = [0] * len(self.cord)
        self.player = 1
        self.placingMen = 0
        self.countMan = [9, 9]

    # placing a men
    def placing(self, pos):
        self.placingMen += 1
        self.board[pos] = self.player

    # moving a men
    def moving(self, pos, topos):
        self.board[pos] = 0
        self.board[topos] = self.player

    # removing a men if mill
    def removing(self, pos):
        self.board[pos] = 0
        if self.player == 1:
            self.countMan[1] -= 1
        else:
            self.countMan[0] -= 1

    # check if mill
    def is_mill(self, index, p):
        mill_map = {
            0: [[1, 2], [9, 21]], 1: [[0, 2], [4, 7]], 2: [[0, 1], [14, 23]],
            3: [[4, 5], [10, 18]], 4: [[3, 5], [1, 7]], 5: [[3, 4], [13, 20]],
            6: [[7, 8], [11, 15]], 7: [[6, 8], [1, 4]], 8: [[6, 7], [12, 17]],
            9: [[10, 11], [0, 21]], 10: [[9, 11], [3, 18]], 11: [[9, 10], [6, 15]],
            12: [[13, 14], [8, 17]], 13: [[12, 14], [5, 20]], 14: [[12, 13], [2, 23]],
            15: [[16, 17], [6, 11]], 16: [[15, 17], [19, 22]], 17: [[15, 16], [8, 12]],
            18: [[19, 20], [3, 10]], 19: [[18, 20], [16, 22]], 20: [[18, 19], [5, 13]],
            21: [[22, 23], [0, 9]], 22: [[21, 23], [16, 19]], 23: [[21, 22], [2, 14]]
        }

        mill_index1 = mill_map[index][0]
        mill_index2 = mill_map[index][1]

        if self.board[mill_index1[0]] == p and self.board[mill_index1[1]] == p:
            return True
        elif self.board[mill_index2[0]] == p and self.board[mill_index2[1]] == p:
            return True
        else:
            return False

    # return adjacent point to index
    def adjacent_pos(self, pos):
        adjacent_map = {
            0: [1, 9], 1: [0, 2, 4], 2: [1, 14],
            3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13],
            6: [7, 11], 7: [4, 6, 8], 8: [7, 12],
            9: [0, 10, 21], 10: [3, 9, 11, 18], 11: [6, 10, 15],
            12: [8, 13, 17], 13: [5, 12, 14, 20], 14: [2, 13, 23],
            15: [11, 16], 16: [15, 17, 19], 17: [12, 16],
            18: [10, 19], 19: [16, 18, 20, 22], 20: [13, 19],
            21: [9, 22], 22: [19, 21, 23], 23: [14, 22],
        }
        return adjacent_map[pos]

    # check if no adjacent point
    def no_adjacent(self):
        count = 0
        for i in range(len(self.board)):
            if self.board[i] == self.player:
                for adj in self.adjacent_pos(i):
                    if self.board[adj] == 0:
                        count += 1
        if count == 0:
            return True
        else:
            return False

    # check if valid point
    def clickable(self, cor, m, size):
        if cor[0] + size >= m[0] >= cor[0] - size and \
                cor[1] + size >= m[1] >= cor[1] - size:
            return True
        else:
            return False
