import pygame as p  # type: ignore
import chessEngine

p.init()
p.display.set_caption("Caïssa Chess")  # Change window title
# Example: using the white king as the icon
icon = p.image.load("logo.png")
p.display.set_icon(icon)

WIDTH = HEIGHT = 512

DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

# global initialization of the images in the main once


def loadImages():
    pieces = ['Wk', 'Wq', 'Wr', 'Wb', 'Wn',
              'Wp', 'Bk', 'Bq', 'Br', 'Bn', 'Bb', 'Bp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )

# this is the main driver code of our program, it'll handle the input and updating the graphics


def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag var for when a move is made
    loadImages()  # only do this once, before the while loop
    running = True
    sqSelected = ()  # no square seleceted rn
    playerClicks = []  # keep track of player clicks

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # gets the (x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):  # the user clicked the same square twice
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear players click
                else:
                    sqSelected = (row, col)
                    # append for both 1st and 2nd clicks
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:  # after 2nd click
                    move = chessEngine.Move(
                        playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()  # reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
                        # key handlers
            elif e.type == p.KEYDOWN and e.key == p.K_z:  # undo when 'z' is pressed
                gs.undoMove()
                moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)  # Call this function to draw the board
        clock.tick(MAX_FPS)
        p.display.flip()

# Responsible for all the graphics within current game state


def drawGameState(screen, gs):
    drawBoard(screen)  # Draw squares on the board
    drawPieces(screen, gs.board)  # Draw pieces on top of the squares

# Draw squares on the board


def drawBoard(screen):
    colors = [p.Color("#EBEBD0"), p.Color("#769454")]
    for r in range(DIMENSION):  # Fixed the incorrect range syntax
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(
                c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(
                    c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
