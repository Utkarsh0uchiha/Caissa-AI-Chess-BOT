# board design (B - Black, W - White) (p - pawn, r - rook, n - knight, q - queen, k - king)
class GameState:
    def __init__(self):
        self.board = [
            ["Br", "Bn", "Bb", "Bq", "Bk", "Bb", "Bn", "Br"],
            ["Bp", "Bp", "Bp", "Bp", "Bp", "Bp", "Bp", "Bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["Wp", "Wp", "Wp", "Wp", "Wp", "Wp", "Wp", "Wp"],
            ["Wr", "Wn", "Wb", "Wq", "Wk", "Wb", "Wn", "Wr"]
        ]
        self.MoveFunc = {'p':
                         self.getPawnMoves, 'r':
                         self.getRookMoves, 'b':
                         self.getBishopMoves, 'n':
                         self.getKnightMoves, 'k':
                         self.getKingMoves, 'q': self.getQueenMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.WhiteKingLocation = (7, 4)
        self.BlackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        # co-ordinates for the square where en-passant is possible
        self.enpassantPossible = ()

    # takes a move asa parameter and executes it (it won't work for pawn promotion and en-passant or castling)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # switch turn

        # if white king moved
        if move.pieceMoved == 'Wk':
            self.WhiteKingLocation = (move.endRow, move.endCol)
        # if black king moved
        elif move.pieceMoved == 'Bk':
            self.BlackKingLocation = (move.endRow, move.endCol)

        # Pawn Promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'q'

        # En-passant capture (remove the opponent's pawn)
        if move.isEnpassantMove:
            # Determine the row of the captured pawn based on the current turn
            captured_pawn_row = move.endRow + 1 if not self.whiteToMove else move.endRow - 1
            self.board[captured_pawn_row][move.endCol] = '--'

        # update enpassantPossible variable
        # Only on 2 square pawn advances
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = (
                (move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

    # undo the last move made

    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turn back

            # if white king moved
            if move.pieceMoved == 'Wk':
                self.WhiteKingLocation = (move.startRow, move.startCol)
            # if black king moved
            elif move.pieceMoved == 'Bk':
                self.BlackKingLocation = (move.startRow, move.startCol)

            # Undo en passant
            if move.isEnpassantMove:
                # Remove the moving pawn from its end position
                self.board[move.endRow][move.endCol] = '--'

                # Restore the captured pawn
                # Determine the captured pawn's row based on the capturing pawn's color
                if move.pieceMoved[0] == 'W':
                    # White pawn captured a black pawn
                    captured_pawn_row = move.endRow + 1
                    self.board[captured_pawn_row][move.endCol] = 'Bp'
                else:
                    # Black pawn captured a white pawn
                    captured_pawn_row = move.endRow - 1
                    self.board[captured_pawn_row][move.endCol] = 'Wp'

            # Undo a 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
    # All the moves considering checks

    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
                if self.whiteToMove:
                    print("BLACK WON!!!")
                else:
                    print("WHITE WON!!!")
            else:
                self.stalemate = True
                print("STALEMATE, DRAW!!!")
        else:
            self.checkmate = False
            self.stalemate = False

        self.enpassantPossible = tempEnpassantPossible
        return moves
    # checks weather the king is in check

    def inCheck(self):
        if self.whiteToMove:
            return self.isSquareAttacked(self.WhiteKingLocation[0], self.WhiteKingLocation[1])
        else:
            return self.isSquareAttacked(self.BlackKingLocation[0], self.BlackKingLocation[1])

    # checks is the square is being attacked or not
    def isSquareAttacked(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppomoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for moves in oppomoves:
            if moves.endRow == r and moves.endCol == c:
                return True
        return False

    # ALl the moves without considering checks

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'W' and self.whiteToMove) or (turn == 'B' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.MoveFunc[piece](r, c, moves)
        return moves

    # get all the pawn moves located at row and col and add these moves to the list

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # White pawn moves UP the board
            if self.board[r - 1][c] == '--':  # Single square move
                moves.append(Move((r, c), (r - 1, c), self.board))
                # Double move from starting position
                if r == 6 and self.board[r - 2][c] == '--':
                    moves.append(Move((r, c), (r - 2, c), self.board))

            # Capture moves (diagonal left and right)
            if c - 1 >= 0:
                # Normal capture
                if self.board[r - 1][c - 1][0] == 'B':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                # En passant capture (left)
                elif self.enpassantPossible == (r - 1, c - 1):
                    moves.append(Move((r, c), (r - 1, c - 1),
                                self.board, isEnpassantMove=True))

            if c + 1 <= 7:
                # Normal capture
                if self.board[r - 1][c + 1][0] == 'B':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                # En passant capture (right)
                elif self.enpassantPossible == (r - 1, c + 1):
                    moves.append(Move((r, c), (r - 1, c + 1),
                                self.board, isEnpassantMove=True))

        else:  # Black pawn moves DOWN the board
            if self.board[r + 1][c] == '--':  # Single square move
                moves.append(Move((r, c), (r + 1, c), self.board))
                # Double move from starting position
                if r == 1 and self.board[r + 2][c] == '--':
                    moves.append(Move((r, c), (r + 2, c), self.board))

            # Capture moves (diagonal left and right)
            if c - 1 >= 0:
                # Normal capture
                if self.board[r + 1][c - 1][0] == 'W':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                # En passant capture (left)
                elif self.enpassantPossible == (r + 1, c - 1):
                    moves.append(Move((r, c), (r + 1, c - 1),
                                self.board, isEnpassantMove=True))

            if c + 1 <= 7:
                # Normal capture
                if self.board[r + 1][c + 1][0] == 'W':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                # En passant capture (right)
                elif self.enpassantPossible == (r + 1, c + 1):
                    moves.append(Move((r, c), (r + 1, c + 1),
                                self.board, isEnpassantMove=True))

    # get all the rook moves located at row and col and add these moves to the list

    def getRookMoves(self, r, c, moves):
        # Moves only in a straight file Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        enemyColor = 'B' if self.whiteToMove else 'W'

        for d in directions:
            for i in range(1, 8):  # Maximum move length is 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Ensure within bounds
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Empty square, valid move
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Enemy piece, valid capture
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                        break  # Stop after capturing
                    else:  # Friendly piece, stop
                        break
                else:  # Out of bounds
                    break

    # get all the  bishop moves located at row and col and add these moves to the list

    def getBishopMoves(self, r, c, moves):
        # moves anywhere diagonally
        directions = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

        enemyColor = 'B' if self.whiteToMove else 'W'

        for d in directions:
            for i in range(1, 8):  # Maximum move length is 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Ensure within bounds
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Empty square, valid move
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Enemy piece, valid capture
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                        break  # Stop after capturing
                    else:  # Friendly piece, stop
                        break
                else:  # Out of bounds
                    break
    # get all the knight moves located at row and col and add these moves to the list

    def getKnightMoves(self, r, c, moves):
        # move 2 and a half squares

        # Possible knight moves (L-shaped jumps)
        knightMoves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        allyColor = 'W' if self.whiteToMove else 'B'

        for d in knightMoves:
            endRow, endCol = r + d[0], c + d[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Ensure move is within bounds
                endPiece = self.board[endRow][endCol]
                # Empty or enemy piece
                if endPiece == "--" or endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # get all the king moves located at row and col and add these moves to the list

    def getKingMoves(self, r, c, moves):
        # moves anywhere but only one square
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, 1), (1, 1), (1, -1), (-1, -1)]

        enemyColor = 'B' if self.whiteToMove else 'W'

        for d in directions:
            for i in range(1, 2):  # Maximum move length is 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Ensure within bounds
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Empty square, valid move
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Enemy piece, valid capture
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                        break  # Stop after capturing
                    else:  # Friendly piece, stop
                        break
                else:  # Out of bounds
                    break
    # get all the queen moves located at row and col and add these moves to the list

    def getQueenMoves(self, r, c, moves):
        # goat piece: can move anywhere on the board
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, 1), (1, 1), (1, -1), (-1, -1)]

        enemyColor = 'B' if self.whiteToMove else 'W'

        for d in directions:
            for i in range(1, 8):  # Maximum move length is 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Ensure within bounds
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Empty square, valid move
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Enemy piece, valid capture
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                        break  # Stop after capturing
                    else:  # Friendly piece, stop
                        break
                else:  # Out of bounds
                    break


class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5,
                   "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2,
                   "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # Pawn Promotion
        self.isPawnPromotion = (self.pieceMoved == 'Wp' and self.endRow == 0) or (
            self.pieceMoved == 'Bp' and self.endRow == 7)
        # En Passant
        self.isEnpassantMove = isEnpassantMove

        self.moveId = self.startRow * 1000 + self.startCol * \
            100 + self.endRow * 10 + self.endCol
    # overwritting the equals method

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def getChessNotation(self):
        # chess notations like 'e2e4', 'e7e5' etc.
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
