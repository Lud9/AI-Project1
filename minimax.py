from unit import Unit
from game import Game, GameType, Player, CoordPair,Options

INFINITY = 99999999

def hasAttackerWon(game: Game) -> bool:
    return game.has_winner() is not None and game.has_winner() == Player.Attacker


def hasDefenderWon(game: Game) -> bool:
    return game.has_winner() is not None and game.has_winner() == Player.Defender

#getting health points
def getHealthPoints(game: Game) -> int:
    score = 0
    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            curUnit = game.board[i][j]
            if curUnit is None:
                continue
            elif curUnit.player == Player.Attacker:
                score += curUnit.health
            else:
                score -= curUnit.health
    return score

'''
similar to health points but also have to account for number of pieces
since 9 total health points with only 1 piece is worse than 9 total health points with 3 pieces
'''
def getNumberOfPieces(game: Game) -> int:
    return 0

#similar to chess where a queen(8) is given more points than a pawn(1) since it is more valuable
def getAttackerPiecePoints(game: Game) -> int:
    return 0

#positive value but it gets substracted after from the score
def getDefenderPiecePoints(game: Game) -> int:
    return 0

'''
2 different functions for attacker & defender piece points because
attacker values some pieces more than others compared to defender
'''
def getPiecePoints(game: Game) -> int:
    return getAttackerPiecePoints(game) - getDefenderPiecePoints(game)

#during each main loop check game state by calling this function to evaluate e(n)
def eScore(game: Game) -> int:
    if hasAttackerWon(game):
        return INFINITY
    elif hasDefenderWon(game):
        return -INFINITY

    else:
        score = 0

        score += getHealthPoints(game)
        score += getNumberOfPieces(game)
        score += getPiecePoints(game)

        #if more than 3 quarters in, give advantage to defender
        if game.turns_played > (3 * game.options.max_turns/4):
            score -= game.turns_played - (3 * game.options.max_turns/4)


    return 0
