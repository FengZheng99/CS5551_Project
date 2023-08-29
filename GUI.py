# Import and initialize the pygame library
import pygame
import board

# initiate
pygame.init()

# 24 points coordination
cord = [(200, 50), (400, 50), (600, 50),
        (266, 116), (400, 116), (534, 116),
        (334, 184), (400, 184), (466, 184),
        (200, 250), (266, 250), (334, 250), (466, 250), (534, 250), (600, 250),
        (334, 316), (400, 316), (466, 316),
        (266, 384), (400, 384), (534, 384),
        (200, 450), (400, 450), (600, 450)
        ]

# initiate the board
board = board.Board(cord)

# Set up the drawing window size and title
screen = pygame.display.set_mode([900, 500])
pygame.display.set_caption("Nine Men Morris")

# images
board_Img = pygame.image.load('board.png')

# some setting
CircleSIZE = 12
smallText = pygame.font.SysFont('Arial', 15)
medianText = pygame.font.SysFont('Arial', 25)
largeText = pygame.font.SysFont('Arial', 35)
winnerText = pygame.font.SysFont('Arial', 70)


# draw board
def drawBoard():
    # display choice of mode
    if HumanMode:
        screen.blit(largeText.render("Human Vs Human", True, (0, 0, 0)), (260, 3))
    elif AiMode:
        screen.blit(largeText.render("Human Vs AI", True, (0, 0, 0)), (270, 3))
    else:
        screen.blit(largeText.render("Choose A Mode", True, (0, 0, 0)), (280, 3))

    # display game stage and turn
    if HumanMode or AiMode:

        # turn
        screen.blit(medianText.render("Turn:", True, (0, 0, 0)), (650, 60))
        if board.player == 1:
            screen.blit(largeText.render("Black", True, (0, 0, 0)), (740, 55))
        elif board.player == -1:
            screen.blit(largeText.render("White", True, (0, 0, 0)), (740, 55))

        # stage
        screen.blit(medianText.render("Stage:", True, (0, 0, 0)), (650, 110))
        if Mill:
            screen.blit(largeText.render("Mill", True, (0, 0, 0)), (740, 105))
        elif board.player == 1 and BlackFlying:
            screen.blit(largeText.render("Flying", True, (0, 0, 0)), (740, 105))
        elif board.player == -1 and WhiteFlying:
            screen.blit(largeText.render("Flying", True, (0, 0, 0)), (740, 105))
        elif Placing:
            screen.blit(largeText.render("Placing", True, (0, 0, 0)), (740, 105))
        elif Moving:
            screen.blit(largeText.render("Moving", True, (0, 0, 0)), (740, 105))

    # draw the men
    for loc in range(len(board.board)):

        # black
        if board.board[loc] == 1:
            x = cord[loc][0]
            y = cord[loc][1]
            pygame.draw.circle(screen, (0, 0, 0), (x, y), CircleSIZE + 1)

        # white
        if board.board[loc] == -1:
            x = cord[loc][0]
            y = cord[loc][1]
            pygame.draw.circle(screen, (255, 255, 255), (x, y), CircleSIZE)
            pygame.draw.circle(screen, (0, 0, 0), (x, y), CircleSIZE + 1, 1)

        # highlight opponent's men if mill
        if Mill:
            if board.player == 1:
                if board.board[loc] == -1:
                    x = cord[loc][0]
                    y = cord[loc][1]
                    pygame.draw.circle(screen, (0, 255, 0), (x, y), CircleSIZE + 5, 3)
            elif board.player == -1:
                if board.board[loc] == 1:
                    x = cord[loc][0]
                    y = cord[loc][1]
                    pygame.draw.circle(screen, (0, 255, 0), (x, y), CircleSIZE + 5, 3)

    # highlight adjacent points
    if Moving and moveFrom is not None:
        for adj in board.adjacentPos(moveFrom):
            if board.board[adj] == 0:
                x = cord[adj][0]
                y = cord[adj][1]
                pygame.draw.circle(screen, (0, 255, 0), (x, y), CircleSIZE + 5, 3)

    # highlight flyable points
    if BlackFlying and board.player == 1 and moveFrom is not None:
        for pos in range(len(cord)):
            if board.board[pos] == 0:
                x = cord[pos][0]
                y = cord[pos][1]
                pygame.draw.circle(screen, (0, 255, 0), (x, y), CircleSIZE + 5, 3)
    elif WhiteFlying and board.player == -1 and moveFrom is not None:
        for pos in range(len(cord)):
            if board.board[pos] == 0:
                x = cord[pos][0]
                y = cord[pos][1]
                pygame.draw.circle(screen, (0, 255, 0), (x, y), CircleSIZE + 5, 3)


# human vs human button
def HvH_button(pos):
    if 30 + 140 > pos[0] > 30 and 50 + 50 > pos[1] > 50:
        pygame.draw.rect(screen, (60, 60, 60), (30, 50, 140, 50))
    else:
        pygame.draw.rect(screen, (30, 30, 30), (30, 50, 140, 50))
    screen.blit(smallText.render("Vs Human", True, (255, 255, 255)), (60, 65))


# human vs AI button
def HvAI_button(pos):
    if 30 + 140 > pos[0] > 30 and 120 + 50 > pos[1] > 120:
        pygame.draw.rect(screen, (60, 60, 60), (30, 120, 140, 50))
    else:
        pygame.draw.rect(screen, (30, 30, 30), (30, 120, 140, 50))
    screen.blit(smallText.render("Vs AI", True, (255, 255, 255)), (75, 135))


# play again page
def playAgain():
    again = True
    while again:

        # get mouse position
        mouse = pygame.mouse.get_pos()

        # check keyboard and mouse event
        for event in pygame.event.get():

            # if click on X top left corner
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # check mouse click
            elif event.type == pygame.MOUSEBUTTONUP:

                # if click on play again
                if 270 + 90 > mouse[0] > 270 and 385 + 50 > mouse[1] > 385:
                    return False

                # if click do not wanna play again
                elif 515 + 90 > mouse[0] > 515 and 385 + 50 > mouse[1] > 385:
                    pygame.quit()
                    quit()

        # draw the page
        screen.fill((255, 193, 37))
        if board.player == 1:
            screen.blit(winnerText.render("White Win!!", True, (0, 0, 0)), (250, 100))
        elif board.player == -1:
            screen.blit(winnerText.render("Black Win!!", True, (0, 0, 0)), (250, 100))
        screen.blit(largeText.render("Play Again?", True, (0, 0, 0)), (350, 300))
        if 270 + 90 > mouse[0] > 270 and 385 + 50 > mouse[1] > 385:
            pygame.draw.rect(screen, (60, 60, 60), (270, 385, 90, 50))
        else:
            pygame.draw.rect(screen, (30, 30, 30), (270, 385, 90, 50))
        if 515 + 90 > mouse[0] > 515 and 385 + 50 > mouse[1] > 385:
            pygame.draw.rect(screen, (60, 60, 60), (515, 385, 90, 50))
        else:
            pygame.draw.rect(screen, (30, 30, 30), (515, 385, 90, 50))
        screen.blit(smallText.render("Yes", True, (255, 255, 255)), (300, 400))
        screen.blit(smallText.render("No", True, (255, 255, 255)), (550, 400))
        pygame.display.update()


# while game is not finish
finish = False
winning = False
while not finish:

    # initiate game setting
    moveFrom = None
    HumanMode = False
    AiMode = False
    Mill = False
    Placing = False
    Moving = False
    BlackFlying = False
    WhiteFlying = False

    # while there is no winner
    while not winning:

        # get mouse position
        mouse = pygame.mouse.get_pos()

        # fill the background, board image, and buttons
        screen.fill((255, 193, 37))
        screen.blit(board_Img, (150, 0))
        HvH_button(mouse)
        HvAI_button(mouse)

        # check each keyboard and mouse action
        for event in pygame.event.get():

            # if click X top left corner, quit the game
            if event.type == pygame.QUIT:
                #winning = True
                #board.player = 0
                pygame.quit()
                quit()

            # if press R, reset the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    HumanMode = False
                    AiMode = False
                    board.reset()

            # check mouse click with its position
            elif event.type == pygame.MOUSEBUTTONUP:

                # when mouse click on human vs human button
                if 30 + 140 > mouse[0] > 30 and 50 + 50 > mouse[1] > 50:
                    HumanMode = True
                    AiMode = False
                    Placing = True
                    Moving = False
                    Flying = False
                    board.reset()

                # when mouse click on human vs AI button
                elif 30 + 140 > mouse[0] > 30 and 120 + 50 > mouse[1] > 120:
                    HumanMode = False
                    AiMode = True
                    Placing = True
                    Moving = False
                    Flying = False
                    board.reset()

                # when mouse click on somewhere else
                elif not HumanMode and not AiMode:
                    continue

                # If form a mill
                elif Mill:
                    for i, c in enumerate(cord):
                        if board.clickable(c, mouse, CircleSIZE) and board.board[i] == board.player * -1:
                            board.removing(i)
                            Mill = False
                            board.changeTurn()

                            # check if number of men of player is equal to 3, turn on flying
                            if board.countMan[0] == 3:
                                BlackFlying = True
                            if board.countMan[1] == 3:
                                WhiteFlying = True

                            # check if number of men of player is less than 3, game over
                            if board.countMan[0] <= 2:
                                print('111white win')
                            elif board.countMan[1] <= 2:
                                print('111black win')

                            # check if adjacent point available, else game over
                            if board.noAdjacent():

                                winning = True
                                if board.player == 1:
                                    print('11white win')
                                else:
                                    print('11black win')

                # flying if black has only 3 men
                elif BlackFlying and board.player == 1:

                    # fly from
                    if moveFrom is None:
                        for i, c in enumerate(cord):
                            if board.clickable(c, mouse, CircleSIZE) and board.board[i] == board.player:
                                moveFrom = i

                    # fly to
                    else:
                        for i, c in enumerate(cord):
                            if board.clickable(c, mouse, CircleSIZE) and i != moveFrom:

                                # change a men to fly
                                if board.board[i] == board.player:
                                    moveFrom = i
                                    break

                                # flying
                                elif board.board[i] == 0:
                                    board.moving(moveFrom, i)

                                # check if form a mill
                                if board.isMill(i, board.player):
                                    Mill = True
                                    moveFrom = None
                                    break

                                # change turn
                                moveFrom = None
                                board.changeTurn()

                # flying if white has only 3 men
                elif WhiteFlying and board.player == -1:

                    # fly from
                    if moveFrom is None:
                        for i, c in enumerate(cord):
                            if board.clickable(c, mouse, CircleSIZE) and board.board[i] == board.player:
                                    moveFrom = i

                    # fly to
                    else:
                        for i, c in enumerate(cord):
                            if board.clickable(c, mouse, CircleSIZE) and i != moveFrom:

                                # change a men to fly
                                if board.board[i] == board.player:
                                    moveFrom = i
                                    break

                                # flying
                                elif board.board[i] == 0:
                                    print('move from ', moveFrom, ' to ', i)
                                    board.moving(moveFrom, i)

                                # check if form a mill
                                if board.isMill(i, board.player):
                                    Mill = True
                                    moveFrom = None
                                    break

                                # change turn
                                moveFrom = None
                                board.changeTurn()

                # placing stage
                elif Placing:
                    for i, c in enumerate(cord):

                        # only empty point can place a men
                        if board.board[i] != 0:
                            print('chose a empty point')
                            continue
                        # placing
                        elif board.clickable(c, mouse, CircleSIZE):
                            board.placing(i)

                            # check if all men is placed
                            if board.placingMen == 18:

                                # if no adjacent point to move, game over
                                if board.noAdjacent():
                                    winning = True
                                    if board.player == 1:
                                        print('1white win')
                                    else:
                                        print('1black win')

                                # switch to moving stage
                                Placing = False
                                Moving = True

                            # check if form a mill
                            if board.isMill(i, board.player):
                                Mill = True
                                break

                            # change turn
                            board.changeTurn()

                # moving stage
                elif Moving:

                    # move from
                    if moveFrom is None:
                        for i, c in enumerate(cord):
                            if board.clickable(c, mouse, CircleSIZE) and board.board[i] == board.player:
                                moveFrom = i

                    # move to
                    else:
                        for i, c in enumerate(cord):
                            if board.clickable(c, mouse, CircleSIZE) and i != moveFrom:

                                # change a men to move
                                if board.board[i] == board.player:
                                    moveFrom = i
                                    break

                                # can only move to adjacent point
                                elif i not in board.adjacentPos(moveFrom):
                                    print('That is not an adjacent point')
                                    break

                                # moving
                                elif board.board[i] == 0 and i in board.adjacentPos(moveFrom):
                                    board.moving(moveFrom, i)

                                # check if form a mill
                                if board.isMill(i, board.player):
                                    Mill = True
                                    moveFrom = None
                                    break

                                # change turn
                                moveFrom = None
                                board.changeTurn()

                                # check if no adjacent, game over
                                if board.noAdjacent():
                                    # winning = True
                                    if board.player == 1:
                                        print('white win')
                                    else:
                                        print('black win')

        # update the display
        drawBoard()
        pygame.display.update()

    # play again page
    winning = playAgain()

pygame.quit()
