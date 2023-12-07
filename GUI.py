# Import standard libraries and custom board class
import os
import random
import time

import pygame

from board import Board

# Initialize the font module
pygame.font.init()

# Font settings as global variables for text display to be called
small_text = pygame.font.SysFont('Arial', 15)
median_text = pygame.font.SysFont('Arial', 25)
large_text = pygame.font.SysFont('Arial', 35)
winner_text = pygame.font.SysFont('Arial', 70)

# Define the coordinates for the 24 points on the Nine Men's Morris board
CORD = [(200, 50), (400, 50), (600, 50),
        (266, 116), (400, 116), (534, 116),
        (334, 184), (400, 184), (466, 184),
        (200, 250), (266, 250), (334, 250),
        (466, 250), (534, 250), (600, 250),
        (334, 316), (400, 316), (466, 316),
        (266, 384), (400, 384), (534, 384),
        (200, 450), (400, 450), (600, 450)
        ]

MILL_TRACK = {
        'm1': 0, 'm2': 0, 'm3': 0, 'm4': 0,
        'm5': 0, 'm6': 0, 'm7': 0, 'm8': 0,
        'm9': 0, 'm10': 0, 'm11': 0, 'm12': 0,
        'm13': 0, 'm14': 0, 'm15': 0, 'm16': 0
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

# Initiate the pygame window
SCREEN = pygame.display.set_mode([900, 500])

# Define game settings
CIRCLE_SIZE = 12 # Size of the circle markers

HUMAN = -1
COMPUTER = 1

non_removeble = []
current_players_men = []
move_from = None
current_move_index = 0  # Variable to track the current move

def computer_move(board):
    global winning

    # Phase 1: Placing pieces
    if board.placed_piece < 18:
        place_random_piece(board)

    # Phase 2: Moving pieces
    elif board.count_piece[1] > 3:
        move_random_piece(board)

    # Phase 3: Flying pieces
    elif board.count_piece[1] == 3:
        fly_random_piece(board)

    if board.count_piece[0] <= 2:
        print('111black win')
        winning = True
        if board.recording == True:
                board.save_recording()
                board.save_recording == False

def place_random_piece(board):
    # Find all empty positions
    valid_positions = [i for i, x in enumerate(board.board) if x == 0]
    
    global available_adj
    available_adj = []

    for index, item in enumerate(board.board):
        if item == board.player:
            for a in ADJACENT_MAP[index]:
                if board.board[a] == 0:
                    available_adj.append(a)

    global available_mill
    available_mill = []

    for index in available_adj:
        for mill_key, mill_value in MILLS.items():
            if index in mill_value:
                if (board.board[mill_value[0]] + board.board[mill_value[1]] + board.board[mill_value[2]]) == 2:
                    available_mill.append(index)

    # Randomly choose a position to place a piece at the start
    if valid_positions and board.placed_piece == 0:
        pos = random.choice(valid_positions)
        board.place_piece(pos)
        # Check for mill formation and remove a piece if formed
        if board.is_mill(pos, board.player):
            remove_opponent_piece(board)

    # Randomly choose an adjacent position to place a piece to form a mill
    elif available_mill:
        pos = random.choice(available_mill)
        board.place_piece(pos)
        # Check for mill formation and remove a piece if formed
        if board.is_mill(pos, board.player):
            remove_opponent_piece(board)

    # Randomly choose an adjacent position to place a piece if a mill is not possible
    elif available_adj:
        pos = random.choice(available_adj)
        board.place_piece(pos)
        # Check for mill formation and remove a piece if formed
        if board.is_mill(pos, board.player):
            remove_opponent_piece(board)

    # Randomly choose an position to place a piece if no adjacent is available
    elif valid_positions:
        pos = random.choice(valid_positions)
        board.place_piece(pos)
        # Check for mill formation and remove a piece if formed
        if board.is_mill(pos, board.player):
            remove_opponent_piece(board)

def move_random_piece(board):
    # Find all possible moves for the computer's pieces
    valid_moves = [(i, adj) for i in range(len(board.board)) if board.board[i] == board.player
                for adj in board.adjacent_pos(i) if board.board[adj] == 0]
    
    global available_adj
    available_adj = []

    for index, item in enumerate(board.board):
        if item == board.player:
            for a in ADJACENT_MAP[index]:
                if board.board[a] == 0:
                    available_adj.append(a)

    global available_mill
    available_mill = []

    for index in available_adj:
        for mill_key, mill_value in MILLS.items():
            if index in mill_value:
                if (board.board[mill_value[0]] + board.board[mill_value[1]] + board.board[mill_value[2]]) == 2:
                    available_mill.append(index)

    mill_moves = []
    adj_moves = []

    for from_pos, to_pos in valid_moves:
        for mill_key, mill_value in MILLS.items():
            if to_pos in available_mill and to_pos in mill_value and from_pos not in mill_value:
                mill_moves.append((from_pos, to_pos))
        if to_pos in available_adj:
            adj_moves.append((from_pos, to_pos))

    # Randomly choose a move, prioritizing mills and adjacents if possible 
    if mill_moves:
        from_pos, to_pos = random.choice(mill_moves)
        board.move_piece(from_pos, to_pos)

        # Check for mill formation and remove a piece if formed
        if board.is_mill(to_pos, board.player):
            remove_opponent_piece(board)
    
    elif adj_moves:
        from_pos, to_pos = random.choice(adj_moves)
        board.move_piece(from_pos, to_pos)

        # Check for mill formation and remove a piece if formed
        if board.is_mill(to_pos, board.player):
            remove_opponent_piece(board)

    elif valid_moves:
        from_pos, to_pos = random.choice(valid_moves)
        board.move_piece(from_pos, to_pos)

        # Check for mill formation and remove a piece if formed
        if board.is_mill(to_pos, board.player):
            remove_opponent_piece(board)


def fly_random_piece(board):
    # Find all possible flies for the computer's pieces
    valid_moves = [(i, adj) for i in range(len(board.board)) if board.board[i] == board.player
                for adj in range(len(board.board)) if board.board[adj] == 0]
    
    global available_adj
    available_adj = []

    for index, item in enumerate(board.board):
        if item == board.player:
            for a in ADJACENT_MAP[index]:
                if board.board[a] == 0:
                    available_adj.append(a)

    global available_mill
    available_mill = []

    for index in available_adj:
        for mill_key, mill_value in MILLS.items():
            if index in mill_value:
                if (board.board[mill_value[0]] + board.board[mill_value[1]] + board.board[mill_value[2]]) == 2:
                    available_mill.append(index)

    mill_moves = []
    adj_moves = []

    for from_pos, to_pos in valid_moves:
        for mill_key, mill_value in MILLS.items():
            if to_pos in available_mill and to_pos in mill_value and from_pos not in mill_value:
                mill_moves.append((from_pos, to_pos))
        if to_pos in available_adj:
            adj_moves.append((from_pos, to_pos))

    # Randomly choose a fly, prioritizing mills and adjacents if possible
    if mill_moves:
        from_pos, to_pos = random.choice(mill_moves)
        board.move_piece(from_pos, to_pos)

        # Check for mill formation and remove a piece if formed
        if board.is_mill(to_pos, board.player):
            remove_opponent_piece(board)
    
    elif adj_moves:
        from_pos, to_pos = random.choice(adj_moves)
        board.move_piece(from_pos, to_pos)

        # Check for mill formation and remove a piece if formed
        if board.is_mill(to_pos, board.player):
            remove_opponent_piece(board)

    elif valid_moves:
        from_pos, to_pos = random.choice(valid_moves)
        board.move_piece(from_pos, to_pos)

        # Check for mill formation and remove a piece if formed
        if board.is_mill(to_pos, board.player):
            remove_opponent_piece(board)


def remove_opponent_piece(board):
    # Choose a random opponent piece that is not in a mill

    global non_removeble
    non_removeble = []

    for mill_key, mill_value in MILLS.items():
        if MILL_TRACK[mill_key] == board.player * -1:
            for pos in mill_value:
                non_removeble.append(pos)

    global current_players_men
    current_players_men = []
    
    for position, man in enumerate(board.board):
        if man == board.player * -1:
            current_players_men.append(position)

    removable = [number for number in current_players_men if number not in non_removeble]

    if removable:
        piece_to_remove = random.choice(removable)
    elif current_players_men:
        piece_to_remove = random.choice(current_players_men)
        
    board.remove_piece(piece_to_remove)

    global white_flying
    if board.count_piece[0] == 3:
        white_flying = True

# Function to draw the game board and status information
def draw_board(board):

    global non_removeble
    global current_players_men

    # Display grid labels
    chars = 'abcdefg'
    for i, char in enumerate(chars):
        SCREEN.blit(small_text.render(char, True, (0, 0, 0)), (195 + 67 * i, 465))
        SCREEN.blit(small_text.render(str(i + 1), True, (0, 0, 0)), (175, 445 - 67 * i))

    # Display the chosen game mode:
    if human_mode:
        SCREEN.blit(large_text.render("Human Vs Human", True, (0, 0, 0)), (260, 3))
    elif computer_mode:
        SCREEN.blit(large_text.render("Human Vs Computer", True, (0, 0, 0)), (260, 3))
    else:
        SCREEN.blit(large_text.render("Choose A Mode", True, (0, 0, 0)), (280, 3))

    # Display current turn and game stage:
    if (human_mode or computer_mode) and board.player != 0:
        # Indicate whose turn it is
        SCREEN.blit(median_text.render("Turn:", True, (0, 0, 0)), (650, 60))
        if board.player == 1:
            SCREEN.blit(large_text.render("Black", True, (0, 0, 0)), (740, 55))
        elif board.player == -1:
            SCREEN.blit(large_text.render("White", True, (0, 0, 0)), (740, 55))

        # Indicate the current game stage
        SCREEN.blit(median_text.render("Stage:", True, (0, 0, 0)), (650, 110))
        if mill: # If a mill has been formed, indicate that the player must remove an opponent's piece
            SCREEN.blit(large_text.render("Mill", True, (0, 0, 0)), (740, 105))
        elif board.player == 1 and black_flying: # If black is in the flying stage
            SCREEN.blit(large_text.render("Flying", True, (0, 0, 0)), (740, 105))
        elif board.player == -1 and white_flying: # If white is in the flying stage
            SCREEN.blit(large_text.render("Flying", True, (0, 0, 0)), (740, 105))
        elif place_piece_stage: # If the game is in the place_piece stage
            SCREEN.blit(large_text.render("Placing", True, (0, 0, 0)), (740, 105))
        elif move_piece_stage: # If the game is in the move_piece stage
            SCREEN.blit(large_text.render("Moving", True, (0, 0, 0)), (740, 105))

    for loc in range(len(board.board)):

        # Draw black men
        if board.board[loc] == 1:
            x = CORD[loc][0]
            y = CORD[loc][1]
            pygame.draw.circle(SCREEN, (0, 0, 0), (x, y), CIRCLE_SIZE + 1)

        # Draw white men
        if board.board[loc] == -1:
            x = CORD[loc][0]
            y = CORD[loc][1]
            pygame.draw.circle(SCREEN, (255, 255, 255), (x, y), CIRCLE_SIZE)
            pygame.draw.circle(SCREEN, (0, 0, 0), (x, y), CIRCLE_SIZE + 1, 1)

        # Highlight opponent's men if a mill is formed
        if mill:
            if board.player == 1:
                if board.board[loc] == -1 and ((loc not in non_removeble) or all(map(lambda x: x in non_removeble, current_players_men))):
                    x = CORD[loc][0]
                    y = CORD[loc][1]
                    pygame.draw.circle(SCREEN, (0, 255, 0), (x, y), CIRCLE_SIZE + 5, 3)
            elif board.player == -1:
                if board.board[loc] == 1 and ((loc not in non_removeble) or all(map(lambda x: x in non_removeble, current_players_men))):
                    x = CORD[loc][0]
                    y = CORD[loc][1]
                    pygame.draw.circle(SCREEN, (0, 255, 0), (x, y), CIRCLE_SIZE + 5, 3)

    #  Highlight points adjacent to the selected men during the move_piece stage
    if move_piece_stage and move_from is not None:
        for adj in board.adjacent_pos(move_from):
            if board.board[adj] == 0:
                x = CORD[adj][0]
                y = CORD[adj][1]
                pygame.draw.circle(SCREEN, (0, 255, 0), (x, y), CIRCLE_SIZE + 5, 3)

    # Highlight all available points when a player can 'fly'
    if black_flying and board.player == 1 and move_from is not None:
        for pos in range(len(CORD)):
            if board.board[pos] == 0:
                x = CORD[pos][0]
                y = CORD[pos][1]
                pygame.draw.circle(SCREEN, (0, 255, 0), (x, y), CIRCLE_SIZE + 5, 3)
    elif white_flying and board.player == -1 and move_from is not None:
        for pos in range(len(CORD)):
            if board.board[pos] == 0:
                x = CORD[pos][0]
                y = CORD[pos][1]
                pygame.draw.circle(SCREEN, (0, 255, 0), (x, y), CIRCLE_SIZE + 5, 3)
    pygame.display.update()

# Function to draw the end game button
def end_button(pos):
    if 20 + 30 > pos[0] > 20 and 10 + 30 > pos[1] > 10:
        pygame.draw.rect(SCREEN, (60, 60, 60), (20, 10, 30, 30))
    else:
        pygame.draw.rect(SCREEN, (30, 30, 30), (20, 10, 30, 30))
    SCREEN.blit(small_text.render("X", True, (255, 255, 255)), (30, 15))

# Function to draw the button for Human vs Human mode
def hvh_button(pos):
    if 20 + 140 > pos[0] > 20 and 50 + 50 > pos[1] > 50:
        pygame.draw.rect(SCREEN, (60, 60, 60), (20, 50, 140, 50))
    else:
        pygame.draw.rect(SCREEN, (30, 30, 30), (20, 50, 140, 50))
    SCREEN.blit(small_text.render("Vs Human", True, (255, 255, 255)), (50, 65))

# Function to draw the button for Human vs Computer mode
def hvcomputer_button(pos):
    if 20 + 140 > pos[0] > 20 and 120 + 50 > pos[1] > 120:
        pygame.draw.rect(SCREEN, (60, 60, 60), (20, 120, 140, 50))
    else:
        pygame.draw.rect(SCREEN, (30, 30, 30), (20, 120, 140, 50))
    SCREEN.blit(small_text.render("Vs Computer", True, (255, 255, 255)), (50, 135))

# Function to draw the button for selecting to play black
def black_button(pos):
    if 620 + 100 > pos[0] > 620 and 50 + 50 > pos[1] > 50:
        pygame.draw.rect(SCREEN, (60, 60, 60), (620, 50, 100, 50))
    else:
        pygame.draw.rect(SCREEN, (30, 30, 30), (620, 50, 100, 50))
    SCREEN.blit(small_text.render("Black", True, (255, 255, 255)), (650, 65))

# Function to draw the button for selecting to play white
def white_button(pos):
    if 620 + 100 > pos[0] > 620 and 120 + 50 > pos[1] > 120:
        pygame.draw.rect(SCREEN, (60, 60, 60), (620, 120, 100, 50))
    else:
        pygame.draw.rect(SCREEN, (30, 30, 30), (620, 120, 100, 50))
    SCREEN.blit(small_text.render("White", True, (255, 255, 255)), (650, 135))

# Function to draw the button for recording game
def record_button(pos):
    if board.recording == False:
        if 30 + 100 > pos[0] > 30 and 400 + 50 > pos[1] > 400:
            pygame.draw.rect(SCREEN, (60, 60, 60), (30, 400, 100, 50))
        else:
            pygame.draw.rect(SCREEN, (30, 30, 30), (30, 400, 100, 50))
        SCREEN.blit(small_text.render("Record", True, (255, 255, 255)), (55, 415))
    else:
        pygame.draw.rect(SCREEN, (255, 0, 0), (30, 400, 100, 50))
        SCREEN.blit(small_text.render("Recording", True, (0, 0, 0)), (48, 415))
        

# Replay button
def replay_button(pos):
    if board.replay == False:
        if 30 + 100 > pos[0] > 30 and 340 + 50 > pos[1] > 340:
            pygame.draw.rect(SCREEN, (60, 60, 60), (30, 340, 100, 50))
        else:
            pygame.draw.rect(SCREEN, (30, 30, 30), (30, 340, 100, 50))
        SCREEN.blit(small_text.render("Replay", True, (255, 255, 255)), (55, 355))
    else:
        pygame.draw.rect(SCREEN, (255, 0, 0), (30, 340, 100, 50))
        SCREEN.blit(small_text.render("Replaying", True, (0, 0, 0)), (48, 355))
        
def forward_button(pos):
    if 620 + 100 > pos[0] > 620 and 340 + 50 > pos[1] > 340:
        pygame.draw.rect(SCREEN, (60, 60, 60), (620, 340, 100, 50))
    else:
        pygame.draw.rect(SCREEN, (30, 30, 30), (620, 340, 100, 50))
    SCREEN.blit(small_text.render("Forward", True, (255, 255, 255)), (640, 355))
        
def backward_button(pos):
    if 620 + 100 > pos[0] > 620 and 400 + 50 > pos[1] > 400:
        pygame.draw.rect(SCREEN, (60, 60, 60), (620, 400, 100, 50))
    else:
        pygame.draw.rect(SCREEN, (30, 30, 30), (620, 400, 100, 50))
    SCREEN.blit(small_text.render("Backward", True, (255, 255, 255)), (640, 415))

# Function to load a page to ask if the user wants to play again
def play_again(board):
    board.save_recording()
    again = True
    while again:

        # Get the current mouse position
        mouse = pygame.mouse.get_pos()

        # Handle events in the game loop
        for event in pygame.event.get():

            # Handle 'Quit' event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Handle mouse click event
            elif event.type == pygame.MOUSEBUTTONUP:

                # Click 'Yes' to play again
                if 270 + 90 > mouse[0] > 270 and 385 + 50 > mouse[1] > 385:
                    board.reset()
                    return False
                # Click 'No' to quit the game
                elif 515 + 90 > mouse[0] > 515 and 385 + 50 > mouse[1] > 385:
                    pygame.quit()
                    quit()

        # Draw elements on the SCREEN
        SCREEN.fill((255, 193, 37))
        if board.player == 1:
            SCREEN.blit(winner_text.render("White Win!!", True, (0, 0, 0)), (250, 100))
        elif board.player == -1:
            SCREEN.blit(winner_text.render("Black Win!!", True, (0, 0, 0)), (250, 100))
        SCREEN.blit(large_text.render("Play Again?", True, (0, 0, 0)), (350, 300))
        if 270 + 90 > mouse[0] > 270 and 385 + 50 > mouse[1] > 385:
            pygame.draw.rect(SCREEN, (60, 60, 60), (270, 385, 90, 50))
        else:
            pygame.draw.rect(SCREEN, (30, 30, 30), (270, 385, 90, 50))
        if 515 + 90 > mouse[0] > 515 and 385 + 50 > mouse[1] > 385:
            pygame.draw.rect(SCREEN, (60, 60, 60), (515, 385, 90, 50))
        else:
            pygame.draw.rect(SCREEN, (30, 30, 30), (515, 385, 90, 50))
        SCREEN.blit(small_text.render("Yes", True, (255, 255, 255)), (300, 400))
        SCREEN.blit(small_text.render("No", True, (255, 255, 255)), (550, 400))
        pygame.display.update()

# Function to auto replay the game
def replaying(board):
    
    directory = "Records/"
    files = os.listdir(directory)
    files.sort()
    last_file = files[-1] if files else None
    
    with open(os.path.join(directory, last_file), 'r') as f:
        moves = f.readlines()
        
    for move in moves:
        move = move.strip('\n').split(' ')
        if move[0] == 'Place':
            board.player = int(move[2])
            board.place_piece(int(move[1]))
        elif move[0] == 'Move':
            board.player = int(move[3])
            board.move_piece(int(move[1]), int(move[2]))
        elif move[0] == 'Remove':
            board.remove_piece(int(move[1]))
        else:
            print("Invalid move")
        if board.auto_replay == True:
            time.sleep(1)
            
        draw_board(board)
        
# Replay manually
def load_replay_moves(filename):
    directory = "Records/"
    files = os.listdir(directory)
    files.sort()
    last_file = files[-1] if files else None
    
    with open(os.path.join(directory, last_file), 'r') as f:
        return [line.strip('\n').split(' ') for line in f.readlines()]

def execute_move(board, move):
    if move[0] == 'Place':
        board.player = int(move[2])
        board.place_piece(int(move[1]))
    elif move[0] == 'Move':
        board.player = int(move[3])
        board.move_piece(int(move[1]), int(move[2]))
    elif move[0] == 'Remove':
        board.remove_piece(int(move[1]))
    else:
        print("Invalid move")
    draw_board(board)

def next_move(board, moves):
    global current_move_index
    if current_move_index < len(moves):
        execute_move(board, moves[current_move_index])
        current_move_index += 1

def previous_move(board, moves):
    global current_move_index
    if current_move_index > 0:
        current_move_index -= 1
        board.reset()  # Resets the board to the initial state
        for move in moves[:current_move_index]:
            execute_move(board, move)

# Function to initiate game settings
def game_settings():
    global move_from
    global human_mode
    global computer_mode
    global mill
    global place_piece_stage
    global move_piece_stage
    global black_flying
    global white_flying
    global MILL_TRACK

    move_from = None
    human_mode = False
    computer_mode = False
    mill = False
    place_piece_stage = False
    move_piece_stage = False
    black_flying = False
    white_flying = False
    MILL_TRACK = {
        'm1': 0, 'm2': 0, 'm3': 0, 'm4': 0,
        'm5': 0, 'm6': 0, 'm7': 0, 'm8': 0,
        'm9': 0, 'm10': 0, 'm11': 0, 'm12': 0,
        'm13': 0, 'm14': 0, 'm15': 0, 'm16': 0
    }

# Function to initiate game settings
def hvh_settings(board):

    global human_mode
    global computer_mode
    global place_piece_stage
    global move_piece_stage
    global black_flying
    global white_flying

    human_mode = True
    computer_mode = False
    place_piece_stage = True
    move_piece_stage = False
    black_flying = False
    white_flying = False
    board.reset()

# Function to initiate game settings
def hvc_settings(board):

    global human_mode
    global computer_mode
    global place_piece_stage
    global move_piece_stage
    global black_flying
    global white_flying

    human_mode = False
    computer_mode = True
    place_piece_stage = True
    move_piece_stage = False
    black_flying = False
    white_flying = False
    board.reset()

# Function to handle the game rules of a mill forming
def mill_rule(board, mouse):

    global MILL_TRACK
    global mill
    global finish
    global winning
    global black_flying
    global white_flying

    for i, c in enumerate(CORD):

        global non_removeble
        non_removeble = []

        for mill_key, mill_value in MILLS.items():
            if MILL_TRACK[mill_key] == board.player * -1:
                for pos in mill_value:
                    non_removeble.append(pos)

        global current_players_men
        current_players_men = []
        
        for position, man in enumerate(board.board):
            if man == board.player * -1:
                current_players_men.append(position)

        if board.clickable(c, mouse, CIRCLE_SIZE) and board.board[i] == board.player * -1 and ((i not in non_removeble) or all(map(lambda x: x in non_removeble, current_players_men))):

            board.remove_piece(i)
            MILL_TRACK = board.mill_list(board.player)
            mill = False
            board.change_turn()

            # check if number of men of player is equal to 3, turn on flying
            if board.count_piece[1] == 3:
                black_flying = True
            if board.count_piece[0] == 3:
                white_flying = True

            # check if number of men of player is less than 3, game over
            if board.count_piece[1] <= 2:
                print('111white win')
                winning = True
                if board.recording == True:
                        board.save_recording()
                        board.save_recording == False
            elif board.count_piece[0] <= 2:
                print('111black win')
                winning = True
                if board.recording == True:
                        board.save_recording()
                        board.save_recording == False

            # check if adjacent point available, else game over
            if board.has_no_valid_moves():

                winning = True
                if board.player == 1:
                    print('11white win')
                else:
                    print('11black win')
                if board.recording == True:
                        board.save_recording()
                        board.save_recording == False
    print(board.board)

# Function to handle the game rule of black flying
def black_fly_rule(board, mouse):

    global MILL_TRACK
    global mill
    global move_from

    # Fly from
    if move_from is None:
        for i, c in enumerate(CORD):
            if board.clickable(c, mouse, CIRCLE_SIZE) and board.board[i] == board.player:
                move_from = i

    # Fly to
    else:
        for i, c in enumerate(CORD):
            if board.clickable(c, mouse, CIRCLE_SIZE) and i != move_from:

                # Change a men to fly
                if board.board[i] == board.player:
                    move_from = i
                    break

                # Flying
                elif board.board[i] == 0:
                    board.move_piece(move_from, i)

                # Check if form a mill
                if board.is_mill(i, board.player):
                    mill = True
                    move_from = None
                    MILL_TRACK = board.mill_list(board.player)
                    break

                # Change turn
                move_from = None
                board.change_turn()
    print(board.board)

# Function to handle the game rule of white flying
def white_fly_rule(board, mouse):
    
    global MILL_TRACK
    global mill
    global move_from
    
    # Fly from
    if move_from is None:
        for i, c in enumerate(CORD):
            if board.clickable(c, mouse, CIRCLE_SIZE) and board.board[i] == board.player:
                move_from = i

    # Fly to
    else:
        for i, c in enumerate(CORD):
            if board.clickable(c, mouse, CIRCLE_SIZE) and i != move_from:

                # Change a men to fly
                if board.board[i] == board.player:
                    move_from = i
                    break

                # Flying
                elif board.board[i] == 0:
                    board.move_piece(move_from, i)

                # Check if form a mill
                if board.is_mill(i, board.player):
                    mill = True
                    move_from = None
                    MILL_TRACK = board.mill_list(board.player)
                    break

                # Change turn
                move_from = None
                board.change_turn()
    print(board.board)

# Function to implement rules of piece placing
def place_piece_rule(board, mouse):

    global move_piece_stage
    global place_piece_stage
    global mill
    global MILL_TRACK
    global winning

    for i, c in enumerate(CORD):
                        
        # Only empty point can place a men
        if board.board[i] != 0:
            print('chose a empty point')
            continue
        # Placing
        elif board.clickable(c, mouse, CIRCLE_SIZE):
            board.place_piece(i)
            print(board.board)
            # Check if all men is placed
            if board.placed_piece == 18:

                # If no adjacent points to move, game over
                if board.has_no_valid_moves():
                    winning = True
                    if board.player == 1:
                        print('1white win')
                    else:
                        print('1black win')
                    if board.recording == True:
                        board.save_recording()
                        board.save_recording == False

                # Switch to move_piece stage
                place_piece_stage = False
                move_piece_stage = True

            # Check if form a mill
            if board.is_mill(i, board.player):
                mill = True
                MILL_TRACK = board.mill_list(board.player)
                break

            # Change turn
            board.change_turn()

# Function to implement rules of piece moving
def move_piece_rule(board, mouse):
    
    global winning
    global mill
    global MILL_TRACK
    global move_from

    # Move from
    if move_from is None:
        for i, c in enumerate(CORD):
            if board.clickable(c, mouse, CIRCLE_SIZE) and board.board[i] == board.player:
                move_from = i

    # Move to
    else:
        for i, c in enumerate(CORD):
            if board.clickable(c, mouse, CIRCLE_SIZE) and i != move_from:

                # Change a men to move
                if board.board[i] == board.player:
                    move_from = i
                    break

                # Can only move to adjacent points
                elif i not in board.adjacent_pos(move_from):
                    print('That is not an adjacent point')
                    break

                # Moving
                elif board.board[i] == 0 and i in board.adjacent_pos(move_from):
                    board.move_piece(move_from, i)

                # Check if form a mill
                if board.is_mill(i, board.player):
                    mill = True
                    move_from = None
                    MILL_TRACK = board.mill_list(board.player)
                    break

                # Change turn
                move_from = None
                board.change_turn()

                # Check if no adjacent points, game over
                if board.has_no_valid_moves():
                    winning = True
                    if board.player == 1:
                        print('white win')
                    else:
                        print('black win')
                    if board.recording == True:
                        board.save_recording()
                        board.save_recording == False
    print(board.board)

# Main Function
def main():

    global move_from
    global human_mode
    global computer_mode
    global mill
    global place_piece_stage
    global move_piece_stage
    global black_flying
    global white_flying
    global MILL_TRACK
    global finish
    global winning
    global move_from
    global starting_player

    # Initiate the game board
    global board
    board = Board(CORD, MILL_TRACK)

    # Configure the pygame window
    pygame.display.set_caption("Nine Men's Morris")

    # Load board image
    board_Img = pygame.image.load('board.png')

    # Main game loop
    finish = False
    winning = False
    starting_player = 0

    while not finish:
        # Initiate game settings
        game_settings()

        # while there is no winner
        while not winning:

            # Get mouse position and handle UI elements
            mouse = pygame.mouse.get_pos()

            # Fill the background, board image, and buttons
            SCREEN.fill((255, 193, 37))
            SCREEN.blit(board_Img, (150, 0))
            end_button(mouse)
            hvh_button(mouse)
            hvcomputer_button(mouse)
            record_button(mouse)
            replay_button(mouse)
            forward_button(mouse)
            backward_button(mouse)
            
            if human_mode:
                if board.player == 0:
                    black_button(mouse)
                    white_button(mouse)
                
            # Handle computer move in computer mode
            elif computer_mode:
                if board.player == 0:
                    board.player = COMPUTER
                if board.player == COMPUTER:
                    computer_move(board)
                    board.player = -board.player
                

            # Event handling loop
            for event in pygame.event.get():

                # Handle 'Quit' event
                if event.type == pygame.QUIT:
                    if board.recording == True:
                        board.save_recording()
                    pygame.quit()
                    quit()

                # Handle 'Reset' key press event
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        human_mode = False
                        computer_mode = False
                        board.reset()

                # Handle mouse click events
                elif event.type == pygame.MOUSEBUTTONUP:

                    # Check if a button is clicked to start the game in a winning state
                    if 20 + 30 > mouse[0] > 20 and 10 + 30 > mouse[1] > 10:
                        winning = True
                        board.player = 0
                        
                        
                    # Check if the human vs human button is clicked
                    elif 20 + 140 > mouse[0] > 20 and 50 + 50 > mouse[1] > 50:
                        hvh_settings(board)

                    # Check if the human vs computer button is clicked
                    elif 20 + 140 > mouse[0] > 20 and 120 + 50 > mouse[1] > 120:
                        hvc_settings(board)

                    # Check if the "Black" button is clicked
                    elif 620 + 100 > mouse[0] > 620 and 50 + 50 > mouse[1] > 50 and board.player == 0:
                        board.player = 1
                        print("Black button clicked")

                    # Check if the "White" button is clicked
                    elif 620 + 100 > mouse[0] > 620 and 120 + 50 > mouse[1] > 120 and board.player == 0:
                        board.player = -1
                        print("White button clicked")

                    # Check if the "Record" button is clicked
                    elif 30 + 100 > mouse[0] > 30 and 400 + 50 > mouse[1] > 400:
                        if board.recording == False:
                            board.recording = True
                        else:
                            board.recording = False

                    elif 180 + 440 > mouse[0] > 180 and 30 + 440 > mouse[1] > 30 and board.player == 0:
                        print("ignore")
                        continue
                    
                    # Check if the "Replay" button is clicked
                    elif 30 + 100 > mouse[0] > 30 and 340 + 50 > mouse[1] > 340:
                        if board.replay == False:
                            board.replay = True
                            board.auto_replay = True
                            replaying(board)
                        else:
                            board.auto_replay = False
                            board.replay = False
                            
                    # Check if the "Forward" button is clicked
                    elif 620 + 100 > mouse[0] > 620 and 340 + 50 > mouse[1] > 340:
                        if board.replay == False:
                            board.replay = True
                            moves = load_replay_moves("Records/game_moves_1.txt")
                            current_move_index = 0
                        else:
                            next_move(board, moves)
                            
                    # Check if the "Backward" button is clicked
                    elif 620 + 100 > mouse[0] > 620 and 400 + 50 > mouse[1] > 400:
                        if board.replay:
                            previous_move(board, moves)
                            draw_board(board)
                            
                    # Check if mouse clicked somewhere other than the available modes
                    elif not human_mode and not computer_mode:
                        continue

                    # Check if a mill formation is detected
                    elif mill:
                        mill_rule(board, mouse)

                    # Handling flying when black has only 3 men
                    elif black_flying and board.player == 1:
                        black_fly_rule(board, mouse)

                    # Handling flying when white has only 3 men
                    elif white_flying and board.player == -1:
                        white_fly_rule(board, mouse)

                    # Handling place_piece stage
                    elif place_piece_stage:
                        place_piece_rule(board, mouse)

                    # Handling move_piece stage
                    elif move_piece_stage:
                        move_piece_rule(board, mouse)

            # Update the display
            draw_board(board)


        # Check if the user wants to play again
        winning = play_again(board)

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
