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

    # takes a move asa parameter and executes it (it won't work for pawn promotion and en-passant or castling)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # black turn

    # undo the last move made
    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turn back

    # All the moves considering checks
    def getValidMoves(self):
        return self.getAllPossibleMoves()

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
            if c - 1 >= 0 and self.board[r - 1][c - 1][0] == 'B':  # Capture left
                moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7 and self.board[r - 1][c + 1][0] == 'B':  # Capture right
                moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # Black pawn moves DOWN the board
            if self.board[r + 1][c] == '--':  # Single square move
                moves.append(Move((r, c), (r + 1, c), self.board))
                # Double move from starting position
                if r == 1 and self.board[r + 2][c] == '--':
                    moves.append(Move((r, c), (r + 2, c), self.board))

            # Capture moves (diagonal left and right)
            if c - 1 >= 0 and self.board[r + 1][c - 1][0] == 'W':  # Capture left
                moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7 and self.board[r + 1][c + 1][0] == 'W':  # Capture right
                moves.append(Move((r, c), (r + 1, c + 1), self.board))

    # get all the rook moves located at row and col and add these moves to the list

    def getRookMoves(self, r, c, moves):
        # Up, Down, Left, Right
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
        pass
    # get all the knight moves located at row and col and add these moves to the list

    def getKnightMoves(self, r, c, moves):
        pass
    # get all the king moves located at row and col and add these moves to the list

    def getKingMoves(self, r, c, moves):
        pass
    # get all the queen moves located at row and col and add these moves to the list

    def getQueenMoves(self, r, c, moves):
        pass


class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5,
                   "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2,
                   "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
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
