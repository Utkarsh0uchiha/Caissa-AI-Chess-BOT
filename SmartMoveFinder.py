import random

pieceScore = {"k": 0, "q": 9, "r": 5, "b": 3, "n": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0  # You might want this to be 0 or some other value based on your strategy
DEPTH = 2


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


# helper method to make first recursive call
def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    MinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove


def MinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreBoard(gs)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = MinMax(gs, nextMove, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = MinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


# a positive score is good for white, a negative score is good for black


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gs.stalemate:
        return STALEMATE
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'W':
                score += pieceScore[square[1].lower()]
            elif square[0] == 'B':
                score -= pieceScore[square[1].lower()]
    return score


def scoreMaterial(board):
    """Evaluate the material value of the position"""
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'W':
                score += pieceScore[square[1].lower()]
            elif square[0] == 'B':
                score -= pieceScore[square[1].lower()]
    return score
