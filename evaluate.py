from unit import Unit
from game import Game
from enums import *

INFINITY = 99999999


def hasAttackerWon(game: Game) -> bool:
    return game.has_winner() is not None and game.has_winner() == Player.Attacker


def hasDefenderWon(game: Game) -> bool:
    return game.has_winner() is not None and game.has_winner() == Player.Defender

def basicEvaluateForAttacker(game: Game) -> int:
    score = 0
    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            curUnit = game.board[i][j]
            if curUnit.player == Player.Attacker:
                if curUnit.type == UnitType.AI:
                    score += 100*curUnit.health
                elif curUnit.type == UnitType.Virus:
                    score += 10*curUnit.health
                elif curUnit.type == UnitType.Tech:
                    score += 10*curUnit.health
                elif curUnit.type == UnitType.Firewall:
                    score += 3*curUnit.health
                elif curUnit.type == UnitType.Program:
                    score += 3*curUnit.health
    return score

def basicEvaluateForDefender(game: Game) -> int:
    score = 0
    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            curUnit = game.board[i][j]
            if curUnit.player == Player.Defender:
                if curUnit.type == UnitType.AI:
                    score += 100 * curUnit.health
                elif curUnit.type == UnitType.Virus:
                    score += 10 * curUnit.health
                elif curUnit.type == UnitType.Tech:
                    score += 10 * curUnit.health
                elif curUnit.type == UnitType.Firewall:
                    score += 3 * curUnit.health
                elif curUnit.type == UnitType.Program:
                    score += 3 * curUnit.health
    return score

def evaluateForAttacker(game: Game) -> int:
    return basicEvaluateForAttacker(game)

def evaluateForDefender(game: Game) -> int:
    return basicEvaluateForDefender(game)

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
            if curUnit.player == Player.Attacker:
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
            elif curUnit.player == Player.Defender:
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
