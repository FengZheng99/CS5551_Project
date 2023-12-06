import os
import random
import time

# Define constants for the game
BLACK = 1
WHITE = -1
INITIAL_PIECES = 9

# Mill combinations and adjacent points for each points map
MILL_MAP = {
            0: [[1, 2], [9, 21]], 1: [[0, 2], [4, 7]], 2: [[0, 1], [14, 23]],
            3: [[4, 5], [10, 18]], 4: [[3, 5], [1, 7]], 5: [[3, 4], [13, 20]],
            6: [[7, 8], [11, 15]], 7: [[6, 8], [1, 4]], 8: [[6, 7], [12, 17]],
            9: [[10, 11], [0, 21]], 10: [[9, 11], [3, 18]], 11: [[9, 10], [6, 15]],
            12: [[13, 14], [8, 17]], 13: [[12, 14], [5, 20]], 14: [[12, 13], [2, 23]],
            15: [[16, 17], [6, 11]], 16: [[15, 17], [19, 22]], 17: [[15, 16], [8, 12]],
            18: [[19, 20], [3, 10]], 19: [[18, 20], [16, 22]], 20: [[18, 19], [5, 13]],
            21: [[22, 23], [0, 9]], 22: [[21, 23], [16, 19]], 23: [[21, 22], [2, 14]]
        }

ADJACENT_MAP = {
            0: [1, 9], 1: [0, 2, 4], 2: [1, 14],
            3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13],
            6: [7, 11], 7: [4, 6, 8], 8: [7, 12],
            9: [0, 10, 21], 10: [3, 9, 11, 18], 11: [6, 10, 15],
            12: [8, 13, 17], 13: [5, 12, 14, 20], 14: [2, 13, 23],
            15: [11, 16], 16: [15, 17, 19], 17: [12, 16],
            18: [10, 19], 19: [16, 18, 20, 22], 20: [13, 19],
            21: [9, 22], 22: [19, 21, 23], 23: [14, 22],
        }

MILLS = {
            'm1': [0, 1, 2], 'm2': [3, 4, 5], 'm3': [6, 7, 8], 'm4': [9, 10, 11],
            'm5': [12, 13, 14], 'm6': [15, 16, 17], 'm7': [18, 19, 20], 'm8': [21, 22, 23],
            'm9': [0, 9, 21], 'm10': [3, 10, 18], 'm11': [6, 11, 15], 'm12': [1, 4, 7],
            'm13': [16, 19, 22], 'm14': [8, 12, 17], 'm15': [5, 13, 20], 'm16': [2, 14, 23]
        }

# Board class to represent the game board
class Board:

    # Initialize the board with its dimensions, player states, and other attributes
    def __init__(self, cord, mill_track):
        self.cord = cord # Coordinates for the board points
        self.board = [0] * len(cord) # Game board represented as a list
        self.mill_track = mill_track # List of mills in the ongoing game
        self.player = 0 # Current player
        self.placed_piece = 0 # Counter for men placed on board
        self.count_piece = [INITIAL_PIECES, INITIAL_PIECES] # Number of men remaining for each player
        self.count_current_piece = [0, 0] # Number of men on the board for each player
        self.recording = False
        self.moves = []
        self.auto_replay = False
        self.replay = False
        self.forward = False
        self.backward = False
        self.replay_moves = [] # List to store the moves for replay
        self.current_replay_index = 0  # Index to track the current move in the replay
    
    # Switch the turn to the other player
    def change_turn(self):
        self.player *= -1

    # Reset the board to its initial state
    def reset(self):
        self.board = [0] * len(self.cord)
        self.player = 0
        self.placed_piece = 0
        self.count_piece = [INITIAL_PIECES, INITIAL_PIECES]
        self.count_current_piece = [0, 0]
        self.mill_track = {
            'm1': 0, 'm2': 0, 'm3': 0, 'm4': 0,
            'm5': 0, 'm6': 0, 'm7': 0, 'm8': 0,
            'm9': 0, 'm10': 0, 'm11': 0, 'm12': 0,
            'm13': 0, 'm14': 0, 'm15': 0, 'm16': 0
        }

    # Place a man at the given position on the board
    def place_piece(self, pos):
        self.placed_piece += 1
        self.board[pos] = self.player
        self.moves.append(f"Place {pos} {self.player}\n")

    # Move a man from one position to another
    def move_piece(self, pos, to_pos):
        self.board[pos] = 0
        self.board[to_pos] = self.player
        self.moves.append(f"Move {pos} {to_pos} {self.player}\n")

    #  Remove a man from the board if a mill condition is met
    def remove_piece(self, pos):

        self.board[pos] = 0
        self.count_piece[0 if self.player == BLACK else 1] -= 1
        self.moves.append(f"Remove {pos}\n")

    # Check if a mill condition is met at the given index for player 'p'
    def is_mill(self, index, p):
        # Checks if a mill condition is met at the given index for player 'p'
        for mill_indices in MILL_MAP[index]:
            if all(self.board[i] == p for i in mill_indices):
                return True
        return False

    # keeping track of mills thoughout the game
    def mill_list(self, p):
        for mill, positions in MILLS.items():
            if all(self.board[pos] == p for pos in positions):
                self.mill_track[mill] = p
            elif all(self.board[pos] == -p for pos in positions):
                self.mill_track[mill] = -p
            else:
                self.mill_track[mill] = 0
        return self.mill_track

    # Return the positions adjacent to the given position 'pos'
    def adjacent_pos(self, pos):
        return ADJACENT_MAP[pos]

    # Check if there are no valid adjacent points to move to for the current player
    def has_no_valid_moves(self):
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
        
    def game_over(self):
        # Flag to indicate if the file needs to be closed
        should_close_file = False
        self.move_file.closed = False
        # Check if the current player has fewer than three pieces on the board
        if self.count_current_piece[0 if self.player == BLACK else 1] < 3:
            print(f"Player {self.player} has fewer than three pieces.")
            should_close_file = True
        # Check if the current player has no legal moves left
        if self.has_no_valid_moves():
            print(f"Player {self.player} has no valid moves.")
            should_close_file = True
        # Close the move_file if it needs to be closed and it's not already closed
        if should_close_file and not self.move_file.closed:
            self.move_file.close()
        return False

    # Check if a click is within a clickable area around a coordinate 'cor'.
    def clickable(self, cor, m, size):
        if cor[0] + size >= m[0] >= cor[0] - size and \
                cor[1] + size >= m[1] >= cor[1] - size:
            return True
        else:
            return False

    # Save the game moves to a file
    def save_recording(self):
        counter = 1
        while os.path.exists("Records/game_moves_%s.txt" % counter):
            counter += 1
        while True:
            save =  open(f"Records/game_moves_{counter}.txt", "w")
            for move in self.moves:
                save.write(move)
            save.close()
            break
        
    # List replay files
    def get_replay_files(directory="Records"):
        return [f for f in os.listdir(directory) if f.endswith('.txt') and f.startswith("game_moves_")]

    # Replaying the game automatically
    def replay_automatically(self, delay):
        filename = self.choose_file()
        if filename:
            self.replay_from_file(filename)
            time.sleep(delay)


