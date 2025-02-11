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
        moves = [Move((6, 4), (4, 4), self.board)]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'W' and self.whiteToMove) and (turn == 'B' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'r':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'b':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'n':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'k':
                        self.getKingMoves(r, c, moves)
                    else:
                        self.getQueenMoves(r, c, moves)
        return moves

    # get all the pawn moves located at row and col and add these moves to the list

    def getPawnMoves(self, r, c, moves):
        pass
    # get all the rook moves located at row and col and add these moves to the list

    def getRookMoves(self, r, c, moves):
        pass
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
