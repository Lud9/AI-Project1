from unit import Unit
from game import Game, GameType, Player, CoordPair,Options

INFINITY = 99999999

def hasAttackerWon(game: Game) -> bool:
    return game.has_winner() is not None and game.has_winner() == Player.Attacker


def hasDefenderWon(game: Game) -> bool:
    return game.has_winner() is not None and game.has_winner() == Player.Defender

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

#during each main loop check game state by calling this function to evaluate e(n)
def eScore(game: Game) -> int:
    if hasAttackerWon(game):
        return INFINITY
    elif hasDefenderWon(game):
        return -INFINITY

    else:
        score = 0

        #getting health points (base heuristic)
        score += getHealthPoints(game)

        #if more than 3 quarters in, give advantage to defender
        if game.turns_played > (3 * game.options.max_turns/4):
            score -= game.turns_played - (3 * game.options.max_turns/4)

        



    return 0
