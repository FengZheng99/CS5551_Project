# Import standard libraries and custom board class
import time
import pygame
import board

# Initialize the pygame engine
pygame.init()

# Define the coordinates for the 24 points on the Nine Men's Morris board
cord = [(200, 50), (400, 50), (600, 50),
        (266, 116), (400, 116), (534, 116),
        (334, 184), (400, 184), (466, 184),
        (200, 250), (266, 250), (334, 250), (466, 250), (534, 250), (600, 250),
        (334, 316), (400, 316), (466, 316),
        (266, 384), (400, 384), (534, 384),
        (200, 450), (400, 450), (600, 450)
        ]

# Initiate the game board
board = board.Board(cord)

# Configure the pygame window
screen = pygame.display.set_mode([900, 500])
pygame.display.set_caption("Nine Men's Morris")

# Load board image
board_Img = pygame.image.load('board.png')

# Define game settings
CIRCLE_SIZE = 12 # Size of the circle markers
# Font settings for text display
small_text = pygame.font.SysFont('Arial', 15)
median_text = pygame.font.SysFont('Arial', 25)
large_text = pygame.font.SysFont('Arial', 35)
winner_text = pygame.font.SysFont('Arial', 70)


# Function to draw the game board and status information
def draw_board():
    # Display grid labels
    chars = 'abcdefg'
    for i, char in enumerate(chars):
        screen.blit(small_text.render(char, True, (0, 0, 0)), (195 + 67 * i, 465))
        screen.blit(small_text.render(str(i + 1), True, (0, 0, 0)), (175, 445 - 67 * i))

    # Display the chosen game mode:
    if human_mode:
        screen.blit(large_text.render("Human Vs Human", True, (0, 0, 0)), (260, 3))
    elif computer_mode:
        screen.blit(large_text.render("Human Vs Computer", True, (0, 0, 0)), (260, 3))
    else:
        screen.blit(large_text.render("Choose A Mode", True, (0, 0, 0)), (280, 3))

    # Display current turn and game stage:
    if human_mode or computer_mode:
        # Indicate whose turn it is
        screen.blit(median_text.render("Turn:", True, (0, 0, 0)), (650, 60))
        if board.player == 1:
            screen.blit(large_text.render("Black", True, (0, 0, 0)), (740, 55))
        elif board.player == -1:
            screen.blit(large_text.render("White", True, (0, 0, 0)), (740, 55))

        # Indicate the current game stage
        screen.blit(median_text.render("Stage:", True, (0, 0, 0)), (650, 110))
        if mill: # If a mill has been formed, indicate that the player must remove an opponent's piece
            screen.blit(large_text.render("Mill", True, (0, 0, 0)), (740, 105))
        elif board.player == 1 and black_flying: # If black is in the flying stage
            screen.blit(large_text.render("Flying", True, (0, 0, 0)), (740, 105))
        elif board.player == -1 and white_flying: # If white is in the flying stage
            screen.blit(large_text.render("Flying", True, (0, 0, 0)), (740, 105))
        elif placing_stage: # If the game is in the placing stage
            screen.blit(large_text.render("Placing", True, (0, 0, 0)), (740, 105))
        elif moving_stage: # If the game is in the moving stage
            screen.blit(large_text.render("Moving", True, (0, 0, 0)), (740, 105))

    # Function to draw the game pieces ('men') on the board
def draw_men():
    for loc in range(len(board.board)):

        # Draw black men
        if board.board[loc] == 1:
            x = cord[loc][0]
            y = cord[loc][1]
            pygame.draw.circle(screen, (0, 0, 0), (x, y), CIRCLE_SIZE + 1)

        # Draw white men
        if board.board[loc] == -1:
            x = cord[loc][0]
            y = cord[loc][1]
            pygame.draw.circle(screen, (255, 255, 255), (x, y), CIRCLE_SIZE)
            pygame.draw.circle(screen, (0, 0, 0), (x, y), CIRCLE_SIZE + 1, 1)

        # Highlight opponent's men if a mill is formed
        if mill:
            if board.player == 1:
                if board.board[loc] == -1:
                    x = cord[loc][0]
                    y = cord[loc][1]
                    pygame.draw.circle(screen, (0, 255, 0), (x, y), CIRCLE_SIZE + 5, 3)
            elif board.player == -1:
                if board.board[loc] == 1:
                    x = cord[loc][0]
                    y = cord[loc][1]
                    pygame.draw.circle(screen, (0, 255, 0), (x, y), CIRCLE_SIZE + 5, 3)

    #  Highlight points adjacent to the selected men during the moving stage
    if moving_stage and move_from is not None:
        for adj in board.adjacent_pos(move_from):
            if board.board[adj] == 0:
                x = cord[adj][0]
                y = cord[adj][1]
                pygame.draw.circle(screen, (0, 255, 0), (x, y), CIRCLE_SIZE + 5, 3)

    # Highlight all available points when a player can 'fly'
    if black_flying and board.player == 1 and move_from is not None:
        for pos in range(len(cord)):
            if board.board[pos] == 0:
                x = cord[pos][0]
                y = cord[pos][1]
                pygame.draw.circle(screen, (0, 255, 0), (x, y), CIRCLE_SIZE + 5, 3)
    elif white_flying and board.player == -1 and move_from is not None:
        for pos in range(len(cord)):
            if board.board[pos] == 0:
                x = cord[pos][0]
                y = cord[pos][1]
                pygame.draw.circle(screen, (0, 255, 0), (x, y), CIRCLE_SIZE + 5, 3)

# Function to draw the end game button
def end_button(pos):
    if 20 + 30 > pos[0] > 20 and 10 + 30 > pos[1] > 10:
        pygame.draw.rect(screen, (60, 60, 60), (20, 10, 30, 30))
    else:
        pygame.draw.rect(screen, (30, 30, 30), (20, 10, 30, 30))
    screen.blit(small_text.render("X", True, (255, 255, 255)), (30, 15))

# Function to draw the button for Human vs Human mode
def hvh_button(pos):
    if 20 + 140 > pos[0] > 20 and 50 + 50 > pos[1] > 50:
        pygame.draw.rect(screen, (60, 60, 60), (20, 50, 140, 50))
    else:
        pygame.draw.rect(screen, (30, 30, 30), (20, 50, 140, 50))
    screen.blit(small_text.render("Vs Human", True, (255, 255, 255)), (50, 65))


# Function to draw the button for Human vs Computer mode
def hvcomputer_button(pos):
    if 20 + 140 > pos[0] > 20 and 120 + 50 > pos[1] > 120:
        pygame.draw.rect(screen, (60, 60, 60), (20, 120, 140, 50))
    else:
        pygame.draw.rect(screen, (30, 30, 30), (20, 120, 140, 50))
    screen.blit(small_text.render("Vs Computer", True, (255, 255, 255)), (50, 135))

# Page to ask if the user wants to play again
def play_again():
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
                    return False
                # Click 'No' to quit the game
                elif 515 + 90 > mouse[0] > 515 and 385 + 50 > mouse[1] > 385:
                    pygame.quit()
                    quit()

        # Draw elements on the screen
        screen.fill((255, 193, 37))
        if board.player == 1:
            screen.blit(winner_text.render("White Win!!", True, (0, 0, 0)), (250, 100))
        elif board.player == -1:
            screen.blit(winner_text.render("Black Win!!", True, (0, 0, 0)), (250, 100))
        screen.blit(large_text.render("Play Again?", True, (0, 0, 0)), (350, 300))
        if 270 + 90 > mouse[0] > 270 and 385 + 50 > mouse[1] > 385:
            pygame.draw.rect(screen, (60, 60, 60), (270, 385, 90, 50))
        else:
            pygame.draw.rect(screen, (30, 30, 30), (270, 385, 90, 50))
        if 515 + 90 > mouse[0] > 515 and 385 + 50 > mouse[1] > 385:
            pygame.draw.rect(screen, (60, 60, 60), (515, 385, 90, 50))
        else:
            pygame.draw.rect(screen, (30, 30, 30), (515, 385, 90, 50))
        screen.blit(small_text.render("Yes", True, (255, 255, 255)), (300, 400))
        screen.blit(small_text.render("No", True, (255, 255, 255)), (550, 400))
        pygame.display.update()

# Main game loop
finish = False
winning = False

while not finish:
    # Initiate game settings
    move_from = None
    human_mode = False
    computer_mode = False
    mill = False
    placing_stage = False
    moving_stage = False
    black_flying = False
    white_flying = False

    # while there is no winner
    while not winning:

        # Get mouse position and handle UI elements
        mouse = pygame.mouse.get_pos()

        # Fill the background, board image, and buttons
        screen.fill((255, 193, 37))
        screen.blit(board_Img, (150, 0))
        end_button(mouse)
        hvh_button(mouse)
        hvcomputer_button(mouse)

        # Event handling loop
        for event in pygame.event.get():

            # Handle 'Quit' event
            if event.type == pygame.QUIT:
                # winning = True
                # board.player = 0
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
                    human_mode = True
                    computer_mode = False
                    placing_stage = True
                    moving_stage = False
                    black_flying = False
                    white_flying = False
                    board.reset()

                # Check if the human vs computer button is clicked
                elif 20 + 140 > mouse[0] > 20 and 120 + 50 > mouse[1] > 120:
                    human_mode = False
                    computer_mode = True
                    placing_stage = True
                    moving_stage = False
                    black_flying = False
                    white_flying = False
                    board.reset()

                # Check if mouse clicked somewhere other than the available modes
                elif not human_mode and not computer_mode:
                    continue

                # Check if a mill formation is detected
                elif mill:
                    for i, c in enumerate(cord):
                        if board.clickable(c, mouse, CIRCLE_SIZE) and board.board[i] == board.player * -1:
                            board.removing(i)
                            mill = False
                            board.change_turn()

                            # check if number of men of player is equal to 3, turn on flying
                            if board.countMan[0] == 3:
                                black_flying = True
                            if board.countMan[1] == 3:
                                white_flying = True

                            # check if number of men of player is less than 3, game over
                            if board.countMan[0] <= 2:
                                print('111white win')
                                winning = True
                            elif board.countMan[1] <= 2:
                                print('111black win')
                                winning = True

                            # check if adjacent point available, else game over
                            if board.no_adjacent():

                                winning = True
                                if board.player == 1:
                                    print('11white win')
                                else:
                                    print('11black win')

                # Handling flying when black has only 3 men
                elif black_flying and board.player == 1:

                    # Fly from
                    if move_from is None:
                        for i, c in enumerate(cord):
                            if board.clickable(c, mouse, CIRCLE_SIZE) and board.board[i] == board.player:
                                move_from = i

                    # Fly to
                    else:
                        for i, c in enumerate(cord):
                            if board.clickable(c, mouse, CIRCLE_SIZE) and i != move_from:

                                # Change a men to fly
                                if board.board[i] == board.player:
                                    move_from = i
                                    break

                                # Flying
                                elif board.board[i] == 0:
                                    board.moving(move_from, i)

                                # Check if form a mill
                                if board.is_mill(i, board.player):
                                    mill = True
                                    move_from = None
                                    break

                                # Change turn
                                move_from = None
                                board.change_turn()

                # Handling flying when white has only 3 men
                elif white_flying and board.player == -1:

                    # Fly from
                    if move_from is None:
                        for i, c in enumerate(cord):
                            if board.clickable(c, mouse, CIRCLE_SIZE) and board.board[i] == board.player:
                                move_from = i

                    # Fly to
                    else:
                        for i, c in enumerate(cord):
                            if board.clickable(c, mouse, CIRCLE_SIZE) and i != move_from:

                                # Change a men to fly
                                if board.board[i] == board.player:
                                    move_from = i
                                    break

                                # Flying
                                elif board.board[i] == 0:
                                    board.moving(move_from, i)

                                # Check if form a mill
                                if board.is_mill(i, board.player):
                                    mill = True
                                    move_from = None
                                    break

                                # Change turn
                                move_from = None
                                board.change_turn()

                # Handling placing stage
                elif placing_stage:
                    for i, c in enumerate(cord):

                        # Only empty point can place a men
                        if board.board[i] != 0:
                            print('chose a empty point')
                            continue
                        # Placing
                        elif board.clickable(c, mouse, CIRCLE_SIZE):
                            board.placing(i)

                            # Check if all men is placed
                            if board.placingMen == 18:

                                # If no adjacent points to move, game over
                                if board.no_adjacent():
                                    winning = True
                                    if board.player == 1:
                                        print('1white win')
                                    else:
                                        print('1black win')

                                # Switch to moving stage
                                placing_stage = False
                                moving_stage = True

                            # Check if form a mill
                            if board.is_mill(i, board.player):
                                mill = True
                                break

                            # Change turn
                            board.change_turn()

                # Handling moving stage
                elif moving_stage:

                    # Move from
                    if move_from is None:
                        for i, c in enumerate(cord):
                            if board.clickable(c, mouse, CIRCLE_SIZE) and board.board[i] == board.player:
                                move_from = i

                    # Move to
                    else:
                        for i, c in enumerate(cord):
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
                                    board.moving(move_from, i)

                                # Check if form a mill
                                if board.is_mill(i, board.player):
                                    mill = True
                                    move_from = None
                                    break

                                # Change turn
                                move_from = None
                                board.change_turn()

                                # Check if no adjacent points, game over
                                if board.no_adjacent():
                                    winning = True
                                    if board.player == 1:
                                        print('white win')
                                    else:
                                        print('black win')

        # Update the display
        draw_board()
        pygame.display.update()

    # Check if the user wants to play again
    winning = play_again()

pygame.quit()
