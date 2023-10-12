from unit import Unit
from game import Game
from coord import *
from enums import *

INFINITY = 99999999


def hasAttackerWon(game: Game) -> bool:
    return game.has_winner() is not None and game.has_winner() == Player.Attacker


def hasDefenderWon(game: Game) -> bool:
    return game.has_winner() is not None and game.has_winner() == Player.Defender

def inOpening(game: Game) -> bool:
    return game.turns_played < (game.options.max_turns/3)

def inEndgame(game: Game) -> bool:
    return game.turns_played > (3*(game.options.max_turns/4))

def basicEvaluateForAttacker(game: Game) -> int:
    score = 0
    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            curUnit = game.board[i][j]
            if curUnit is not None and curUnit.player == Player.Attacker:
                if curUnit.type == UnitType.AI:
                    score += 100 * curUnit.health
                elif curUnit.type == UnitType.Virus:
                    score += 10 * curUnit.health
                elif curUnit.type == UnitType.Tech:
                    score += 10 * curUnit.health
                elif curUnit.type == UnitType.Firewall:
                    score += 5 * curUnit.health
                elif curUnit.type == UnitType.Program:
                    score += 5 * curUnit.health
    return score

def getDefenderAICoord(game: Game) -> int:
    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            curUnit = game.board[i][j]
            if curUnit is not None and curUnit.player == Player.Defender and curUnit.type == UnitType.AI:
                return Coord(i,j)


def moveAttackingPiecesTowardsEnemyAIScore(game: Game) -> int:
    score = 0
    enemyAICoord = getDefenderAICoord(game)

    for row in range(len(game.board)):
        for col in range(len(game.board[row])):
            curUnit = game.board[row][col]
            if curUnit is not None and curUnit.player == Player.Attacker:
                multiplier = 2
                score += multiplier * ((enemyAICoord.row - abs(enemyAICoord.row - row)) + (enemyAICoord.col - abs(enemyAICoord.col - col)))
    return score

def attackerPiecesTogetherScore(game: Game) -> int:
    score = 0
    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            curUnit = game.board[i][j]
            if curUnit is not None and curUnit.player == Player.Attacker:
                srcCoord = Coord(i, j)
                for dstCoord in srcCoord.iter_adjacent():
                    if game.is_valid_coord(dstCoord):
                        adjUnit = game.board[dstCoord.row][dstCoord.col]
                        if adjUnit is not None:
                            if adjUnit.player == Player.Attacker:
                                score += 1
                            if curUnit.type == UnitType.Program and adjUnit.type == UnitType.Virus:
                                score += 10
    return score

def basicEvaluateForDefender(game: Game) -> int:
    score = 0
    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            curUnit = game.board[i][j]
            if curUnit is not None and curUnit.player == Player.Defender:
                if curUnit.type == UnitType.AI:
                    score += 100 * curUnit.health
                elif curUnit.type == UnitType.Virus:
                    score += 10 * curUnit.health
                elif curUnit.type == UnitType.Tech:
                    score += 10 * curUnit.health
                elif curUnit.type == UnitType.Firewall:
                    score += 5 * curUnit.health
                elif curUnit.type == UnitType.Program:
                    score += 5 * curUnit.health
    return score

def closeToFinishScore(game: Game) -> int:
    return game.turns_played - (3*(game.options.max_turns/4))


def evaluateForAttacker(game: Game) -> int:
    score = 0
    score += basicEvaluateForAttacker(game)
    score += moveAttackingPiecesTowardsEnemyAIScore(game)
    attackerPiecesTogetherMultiplier = 0
    if inOpening(game):
        attackerPiecesTogetherMultiplier = 1
    else:
        attackerPiecesTogetherMultiplier = 5
    score += attackerPiecesTogetherMultiplier * attackerPiecesTogetherScore(game)
    return score


def evaluateForDefender(game: Game) -> int:
    score = 0
    score += basicEvaluateForDefender(game)
    #keep num of adjacent coords as small as possible (specifically for ai)
    #keep num of defender pieces in adjacent coords as high as possible (specifically for ai)
    #keep pieces together (specifically tech & program)
    if inEndgame(game):
        score += closeToFinishScore(game)
    return score

#not fully optimized rn will optimize later rn just wna have everything split up
def evaluateScore(game: Game) -> int:
    if hasAttackerWon(game):
        return INFINITY
    elif hasDefenderWon(game):
        return -INFINITY

    else:
        return evaluateForAttacker(game) - evaluateForDefender(game)


'''
e0 in assignment description
'''
def evaluateScore0(game: Game) -> int:
    score = 0
    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            curUnit = game.board[i][j]
            if curUnit is not None and curUnit.player == Player.Attacker:
                if curUnit.type == UnitType.AI:
                    score += 9999
                elif curUnit.type == UnitType.Virus:
                    score += 3
                elif curUnit.type == UnitType.Tech:
                    score += 3
                elif curUnit.type == UnitType.Firewall:
                    score += 3
                elif curUnit.type == UnitType.Program:
                    score += 3
            elif curUnit is not None and curUnit.player == Player.Defender:
                if curUnit.type == UnitType.AI:
                    score -= 9999
                elif curUnit.type == UnitType.Virus:
                    score -= 3
                elif curUnit.type == UnitType.Tech:
                    score -= 3
                elif curUnit.type == UnitType.Firewall:
                    score -= 3
                elif curUnit.type == UnitType.Program:
                    score -= 3
    return score
