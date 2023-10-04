# Board class
class Board:

    # Initialize the board with its dimensions, player states, and other attributes
    def __init__(self, cord, mill_track):
        self.cord = cord # Coordinates for the board points
        self.board = [0] * len(cord) # Game board represented as a list
        self.mill_track = mill_track # List of mills in the ongoing game
        self.player = 1 # Current player (1 or -1)
        self.placingMen = 0 # Counter for men placed on board
        self.countMan = [0, 9, 9] # Number of men remaining for each player
        self.countCurMan = [0, 0, 0] # Number of men on the board for each player

    # Switch the turn to the other player
    def change_turn(self):
        self.player *= -1

    # Reset the board to its initial state
    def reset(self):
        self.board = [0] * len(self.cord)
        self.player = 1
        self.placingMen = 0
        self.countMan = [0, 9, 9]
        self.countCurMan = [0, 0, 0]
        self.mill_track = {
            'm1': 0, 'm2': 0, 'm3': 0, 'm4': 0,
            'm5': 0, 'm6': 0, 'm7': 0, 'm8': 0,
            'm9': 0, 'm10': 0, 'm11': 0, 'm12': 0,
            'm13': 0, 'm14': 0, 'm15': 0, 'm16': 0
        }

    # Place a man at the given position on the board
    def placing(self, pos):
        self.placingMen += 1
        self.board[pos] = self.player
        self.countCurMan[self.player] += 1
        print(self.countCurMan)

    # Move a man from one position to another
    def moving(self, pos, topos):
        self.board[pos] = 0
        self.board[topos] = self.player

    #  Remove a man from the board if a mill condition is met
    def removing(self, pos):

        self.board[pos] = 0
        self.countCurMan[self.player] -= 1

        if self.player == 1:
            self.countMan[-1] -= 1
        else:
            self.countMan[1] -= 1

    # Check if a mill condition is met at the given index for player 'p'
    def is_mill(self, index, p):

        # Map for all possible mill combinations
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

        # Extract the mill indices based on the given index
        mill_index1 = mill_map[index][0]
        mill_index2 = mill_map[index][1]

        if self.board[mill_index1[0]] == p and self.board[mill_index1[1]] == p:
            return True
        elif self.board[mill_index2[0]] == p and self.board[mill_index2[1]] == p:
            return True
        else:
            return False

    # keeping track of mills thoughout the game
    def mill_list(self, index, p):

        mills = {
            'm1': [0, 1, 2], 'm2': [3, 4, 5], 'm3': [6, 7, 8], 'm4': [9, 10, 11],
            'm5': [12, 13, 14], 'm6': [15, 16, 17], 'm7': [18, 19, 20], 'm8': [21, 22, 23],
            'm9': [0, 9, 21], 'm10': [3, 10, 18], 'm11': [6, 11, 15], 'm12': [1, 4, 7],
            'm13': [16, 19, 22], 'm14': [8, 12, 17], 'm15': [5, 13, 20], 'm16': [2, 14, 23]
        }
        
        for mill, positions in mills.items():
            if index in positions:
                if all(self.board[pos] == p for pos in positions):
                    self.mill_track[mill] = p

        return self.mill_track

    # Return the positions adjacent to the given position 'pos'
    def adjacent_pos(self, pos):
        # Map for all possible adjacent points
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

    # Check if there are no valid adjacent points to move to for the current player
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

    # Check if a click is within a clickable area around a coordinate 'cor'.
    def clickable(self, cor, m, size):
        if cor[0] + size >= m[0] >= cor[0] - size and \
                cor[1] + size >= m[1] >= cor[1] - size:
            return True
        else:
            return False
