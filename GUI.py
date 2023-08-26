# Import and initialize the pygame library
import pygame
import board

# initiate
pygame.init()

# Set up the drawing window size and title
screen = pygame.display.set_mode([800, 500])
pygame.display.set_caption("Nine Men Morris")

# images
board_Img = pygame.image.load('board.png')

# 24 points coordination
cord = [(200, 50), (400, 50), (600, 50),
        (266, 116), (400, 116), (534, 116),
        (334, 184), (400, 184), (466, 184),
        (200, 250), (266, 250), (334, 250), (466, 250), (534, 250), (600, 250),
        (334, 316), (400, 316), (466, 316),
        (266, 384), (400, 384), (534, 384),
        (200, 450), (400, 450), (600, 450)
        ]

board = board.Board(cord)
numMen = 18
CircleSIZE = 15
smallText = pygame.font.SysFont('Arial', 15)


# draw board
def drawBoard():
    for loc in range(len(board.board)):
        if board.board[loc] == 1:
            x = cord[loc][0]
            y = cord[loc][1]
            pygame.draw.circle(screen, (0, 0, 0), (x, y), CircleSIZE)
        if board.board[loc] == -1:
            x = cord[loc][0]
            y = cord[loc][1]
            pygame.draw.circle(screen, (255, 255, 255), (x, y), CircleSIZE)

        # highlight opponent's men if mill
        if Mill and Placing:
            if board.player == 1:
                if board.board[loc] == -1:
                    x = cord[loc][0]
                    y = cord[loc][1]
                    pygame.draw.circle(screen, (0, 255, 0), (x, y), CircleSIZE+10, 3)
            elif board.player == -1:
                if board.board[loc] == 1:
                    x = cord[loc][0]
                    y = cord[loc][1]
                    pygame.draw.circle(screen, (0, 255, 0), (x, y), CircleSIZE+10, 3)
        elif Mill and Moving:
            print("Some Action")


def HvH_button(pos):
    if 30 + 140 > pos[0] > 30 and 50 + 50 > pos[1] > 50:
        pygame.draw.rect(screen, (60, 60, 60), (30, 50, 140, 50))
    else:
        pygame.draw.rect(screen, (30, 30, 30), (30, 50, 140, 50))
    screen.blit(smallText.render("Vs Human", True, (255, 255, 255)), (60, 65))


def HvAI_button(pos):
    if 30 + 140 > pos[0] > 30 and 120 + 50 > pos[1] > 120:
        pygame.draw.rect(screen, (60, 60, 60), (30, 120, 140, 50))
    else:
        pygame.draw.rect(screen, (30, 30, 30), (30, 120, 140, 50))
    screen.blit(smallText.render("Vs AI", True, (255, 255, 255)), (75, 135))


def clickable(cor, m):
    if cor[0] + CircleSIZE >= m[0] >= cor[0] - CircleSIZE and \
            cor[1] + CircleSIZE >= m[1] >= cor[1] - CircleSIZE:
        return True
    else:
        return False


# Run until the user asks to quit
running = True
HumanMode = False
AiMode = False
Mill = False
Placing = True
Moving = False
Flying = False

while running:
    screen.fill((255, 193, 37))
    screen.blit(board_Img, (150, 0))

    mouse = pygame.mouse.get_pos()
    HvH_button(mouse)
    HvAI_button(mouse)
    for i in range(len(cord)):
        screen.blit(smallText.render(str(i), True, (255, 0, 0)), (cord[i][0]+5, cord[i][1]-20))
    # check mouse event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board.reset()
        elif event.type == pygame.MOUSEBUTTONUP:
            if 30 + 140 > mouse[0] > 30 and 50 + 50 > mouse[1] > 50:
                HumanMode = True
                AiMode = False
                print("Play against Human")
                board.reset()
            elif 30 + 140 > mouse[0] > 30 and 120 + 50 > mouse[1] > 120:
                HumanMode = False
                AiMode = True
                print("Play against Ai")
                board.reset()
            elif not HumanMode and not AiMode:
                print("Choose a mode")

            elif Placing and not Mill:
                for i, c in enumerate(cord):
                    if board.board[i] != 0:
                        continue
                    elif clickable(c, mouse):
                        board.placing(i)
                        if board.placingMen == 18:
                            Placing = False
                            Moving = True
                        if board.isMill(i, board.player):
                            Mill = True
                            break
                        board.changeTurn()
            elif Moving and not Mill:
                for i, c in enumerate(cord):
                    if clickable(c, mouse):
                        a = 0
            elif Mill:
                for i, c in enumerate(cord):
                    if clickable(c, mouse) and board.board[i] == board.player * -1:
                        board.removing(i)
                        Mill = False
                        board.changeTurn()

    drawBoard()

    # update the display
    pygame.display.update()

pygame.quit()
