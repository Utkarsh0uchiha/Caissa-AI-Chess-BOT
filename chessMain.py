import pygame as p  # type: ignore
import chessEngine
import SmartMoveFinder

p.init()
p.display.set_caption("Caïssa Chess")
icon = p.image.load("logo.png")
p.display.set_icon(icon)

# Define colors for a cleaner aesthetic
LIGHT_SQUARE = "#F0D9B5"  # Soft beige
DARK_SQUARE = "#B58863"   # Warm brown
BG_COLOR = "#2C3E50"      # Dark blue-gray
HIGHLIGHT_COLOR = (170, 162, 58, 100)  # Golden yellow with transparency
LAST_MOVE_COLOR = (100, 111, 159, 120)  # Soft blue with transparency
TEXT_COLOR = "#ECF0F1"    # Off-white
BUTTON_COLOR = "#34495E"  # Darker blue-gray
BUTTON_HOVER = "#4A5C6B"  # Lighter when hovered
ACCENT_COLOR = "#3498DB"  # Bright blue for accents

# Board dimensions
WIDTH = HEIGHT = 560
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60  # Smoother animations

# Add padding around the board
PADDING = 40
WINDOW_WIDTH = WIDTH + PADDING * 2

# Button dimensions
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20

# Bottom panel for buttons and status
PANEL_HEIGHT = 80
WINDOW_HEIGHT = HEIGHT + PADDING * 2 + PANEL_HEIGHT

# Global variables
IMAGES = {}
game_over = False
game_result = ""


def loadImages():
    pieces = ['Wk', 'Wq', 'Wr', 'Wb', 'Wn',
              'Wp', 'Bk', 'Bq', 'Br', 'Bn', 'Bb', 'Bp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )

# Check if mouse is over a button


def is_over_button(pos, button_rect):
    return button_rect.collidepoint(pos)

# Draw a button with hover effect


def draw_button(screen, rect, text, font, hover=False):
    color = BUTTON_HOVER if hover else BUTTON_COLOR
    p.draw.rect(screen, p.Color(color), rect, border_radius=5)
    text_surf = font.render(text, True, p.Color(TEXT_COLOR))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


def main():
    global game_over, game_result

    screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = p.time.Clock()

    # Create modern, clean fonts
    button_font = p.font.SysFont("Segoe UI", 16)
    result_font = p.font.SysFont("Segoe UI", 20, bold=True)

    # Initialize game state
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    isUndo = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    playerOne = True  # if human is playing white, then this will be True, If an AI is Playing then it will be false
    playerTwo = False  # same as above but for black

    # Create button rectangles
    reset_button = p.Rect(
        WINDOW_WIDTH//2 - BUTTON_WIDTH - BUTTON_MARGIN//2,
        HEIGHT + PADDING * 2 + PANEL_HEIGHT//2 - BUTTON_HEIGHT//2,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )

    undo_button = p.Rect(
        WINDOW_WIDTH//2 + BUTTON_MARGIN//2,
        HEIGHT + PADDING * 2 + PANEL_HEIGHT//2 - BUTTON_HEIGHT//2,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )

    # Track button hover states
    reset_hover = False
    undo_hover = False

    # Function to reset the game
    def resetGame():
        nonlocal gs, validMoves, moveMade, sqSelected, playerClicks
        global game_over, game_result
        gs = chessEngine.GameState()
        validMoves = gs.getValidMoves()
        moveMade = False
        sqSelected = ()
        playerClicks = []
        game_over = False
        game_result = ""

    while running:
        mouse_pos = p.mouse.get_pos()

        # Update button hover states
        reset_hover = is_over_button(mouse_pos, reset_button)
        undo_hover = is_over_button(mouse_pos, undo_button)
        humanTurn = (gs.whiteToMove and playerOne) or (
            not gs.whiteToMove and playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()

                # Check if reset button was clicked
                if is_over_button(location, reset_button):
                    resetGame()
                    continue

                # Check if undo button was clicked
                if is_over_button(location, undo_button) and len(gs.moveLog) > 0:
                    gs.undoMove()
                    moveMade = True
                    isUndo = True
                    game_over = False
                    game_result = ""
                    continue

                # Process board clicks only if game is not over
                if not game_over and humanTurn:
                    # Adjust for padding to get board coordinates
                    board_x = location[0] - PADDING
                    board_y = location[1] - PADDING

                    # Check if click is within the board
                    if 0 <= board_x < WIDTH and 0 <= board_y < HEIGHT:
                        col = board_x // SQ_SIZE
                        row = board_y // SQ_SIZE

                        if sqSelected == (row, col):  # Clicked same square twice
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)

                        if len(playerClicks) == 2:  # After 2nd click
                            move = chessEngine.Move(
                                playerClicks[0], playerClicks[1], gs.board)

                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    isUndo = False
                                    sqSelected = ()
                                    playerClicks = []

                            if not moveMade:
                                playerClicks = [sqSelected]

            # Key handlers (keeping Z as keyboard shortcut for undo)
            elif e.type == p.KEYDOWN and e.key == p.K_z and len(gs.moveLog) > 0:
                gs.undoMove()
                moveMade = True
                isUndo = True
                game_over = False
                game_result = ""

        # AI move finder logic
        if not game_over and not humanTurn:
            AIMove = SmartMoveFinder.findBestMoveNegaMax(gs, validMoves)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
            if not isUndo and len(gs.moveLog) > 0:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            isUndo = False

            # Check for game end conditions
            if gs.checkmate:
                game_over = True
                if gs.whiteToMove:
                    game_result = "Black Wins by Checkmate"
                else:
                    game_result = "White Wins by Checkmate"
            elif gs.stalemate:
                game_over = True
                game_result = "Draw by Stalemate"

        # Draw everything
        screen.fill(p.Color(BG_COLOR))

        # Draw board with padding
        drawGameState(screen, gs, validMoves, sqSelected)

        # Draw buttons
        draw_button(screen, reset_button, "New Game", button_font, reset_hover)
        draw_button(screen, undo_button, "Undo Move", button_font, undo_hover)

        # Display turn indicator
        turn_text = "White to Move" if gs.whiteToMove else "Black to Move"
        turn_surf = button_font.render(turn_text, True, p.Color(TEXT_COLOR))
        turn_rect = turn_surf.get_rect(
            center=(WINDOW_WIDTH//2, HEIGHT + PADDING + 20))
        screen.blit(turn_surf, turn_rect)

        # Display game result if game is over
        if game_over:
            # Create semi-transparent overlay for game over message
            overlay = p.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(p.Color(BG_COLOR))
            screen.blit(overlay, (PADDING, PADDING))

            result_surf = result_font.render(
                game_result, True, p.Color(TEXT_COLOR))
            result_rect = result_surf.get_rect(
                center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 20))
            screen.blit(result_surf, result_rect)

            # Add prompt to restart
            prompt_surf = button_font.render(
                "Click 'New Game' to play again", True, p.Color(TEXT_COLOR))
            prompt_rect = prompt_surf.get_rect(
                center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
            screen.blit(prompt_surf, prompt_rect)

        p.display.flip()
        clock.tick(MAX_FPS)


def highlightSquares(screen, gs, validMoves, sqSelected):
    # Highlight last move
    if gs.moveLog:
        lastMove = gs.moveLog[-1]
        last_move_s = p.Surface((SQ_SIZE, SQ_SIZE))
        last_move_s.fill(p.Color(LAST_MOVE_COLOR))

        # Highlight both squares of last move
        screen.blit(last_move_s, (PADDING + lastMove.startCol *
                    SQ_SIZE, PADDING + lastMove.startRow*SQ_SIZE))
        screen.blit(last_move_s, (PADDING + lastMove.endCol *
                    SQ_SIZE, PADDING + lastMove.endRow*SQ_SIZE))

    # Highlight selected square and valid moves
    if sqSelected != ():
        r, c = sqSelected

        # Check if the selected piece belongs to the current player
        if gs.board[r][c][0] == ('W' if gs.whiteToMove else 'B'):
            # Create highlighting surface
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color(HIGHLIGHT_COLOR))

            # Highlight selected square
            screen.blit(s, (PADDING + c*SQ_SIZE, PADDING + r*SQ_SIZE))

            # Highlight valid moves from that square with subtle circles
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    if gs.board[move.endRow][move.endCol] == '--':
                        # Empty square - draw circle
                        radius = SQ_SIZE // 6
                        center = (PADDING + move.endCol*SQ_SIZE + SQ_SIZE//2,
                                  PADDING + move.endRow*SQ_SIZE + SQ_SIZE//2)
                        p.draw.circle(screen, p.Color(
                            HIGHLIGHT_COLOR), center, radius)
                    else:
                        # Capture square - draw ring
                        s.set_alpha(180)
                        screen.blit(s, (PADDING + move.endCol *
                                    SQ_SIZE, PADDING + move.endRow*SQ_SIZE))
                        inner = p.Surface((SQ_SIZE*0.8, SQ_SIZE*0.8))
                        inner.fill(
                            p.Color(colors[(move.endRow + move.endCol) % 2]))
                        inner_pos = (PADDING + move.endCol*SQ_SIZE + SQ_SIZE*0.1,
                                     PADDING + move.endRow*SQ_SIZE + SQ_SIZE*0.1)
                        screen.blit(inner, inner_pos)


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

    # Draw border around the board
    border_rect = p.Rect(PADDING-2, PADDING-2, WIDTH+4, HEIGHT+4)
    p.draw.rect(screen, p.Color(ACCENT_COLOR), border_rect, 2, border_radius=3)


def drawBoard(screen):
    global colors
    colors = [p.Color(LIGHT_SQUARE), p.Color(DARK_SQUARE)]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(
                PADDING + c * SQ_SIZE, PADDING + r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

            # Optional: Add subtle rank/file notation
            if r == 7:  # Bottom rank
                if (r + c) % 2 == 0:
                    text_color = p.Color(DARK_SQUARE)
                else:
                    text_color = p.Color(LIGHT_SQUARE)

                file_font = p.font.SysFont("Segoe UI", 12)
                file_text = file_font.render(
                    chr(ord('a') + c), True, text_color)
                screen.blit(file_text, (PADDING + c *
                            SQ_SIZE + 5, PADDING + HEIGHT - 15))

            if c == 0:  # Left file
                if (r + c) % 2 == 0:
                    text_color = p.Color(DARK_SQUARE)
                else:
                    text_color = p.Color(LIGHT_SQUARE)

                rank_font = p.font.SysFont("Segoe UI", 12)
                rank_text = rank_font.render(str(8-r), True, text_color)
                screen.blit(rank_text, (PADDING + 5,
                            PADDING + r * SQ_SIZE + 5))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(
                    PADDING + c * SQ_SIZE, PADDING + r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animateMove(move, screen, board, clock):
    """Animates a chess piece moving from start to end position with smooth motion"""
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol

    # Optimize animation speed and smoothness
    fps = 60  # Target fps for smooth animation
    duration = 0.2  # Animation duration in seconds
    frameCount = int(fps * duration)

    # Get the moving piece
    movingPiece = move.pieceMoved

    # Create a copy of the board for animation
    tempBoard = [row[:] for row in board]
    # Temporarily remove the piece from the board
    tempBoard[move.startRow][move.startCol] = "--"

    # Pre-render the static board background once
    staticBG = p.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    staticBG.fill(p.Color(BG_COLOR))
    drawBoard(staticBG)

    # Draw border around the board
    border_rect = p.Rect(PADDING-2, PADDING-2, WIDTH+4, HEIGHT+4)
    p.draw.rect(staticBG, p.Color(ACCENT_COLOR),
                border_rect, 2, border_radius=3)

    # Draw all non-moving pieces on the static background
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = tempBoard[row][col]
            if piece != "--":
                staticBG.blit(IMAGES[piece], p.Rect(
                    PADDING + col * SQ_SIZE, PADDING + row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Calculate the step size for smooth motion
    stepR = dR / frameCount if frameCount > 0 else dR
    stepC = dC / frameCount if frameCount > 0 else dC

    # Animation loop
    for frame in range(frameCount + 1):
        # Calculate the position for this frame using float for smoother interpolation
        r = move.startRow + stepR * frame
        c = move.startCol + stepC * frame

        # Draw the static background (includes board and non-moving pieces)
        screen.blit(staticBG, (0, 0))

        # Draw the moving piece at its current position
        screen.blit(IMAGES[movingPiece], p.Rect(
            PADDING + c * SQ_SIZE, PADDING + r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        # Update the display and maintain framerate
        p.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
