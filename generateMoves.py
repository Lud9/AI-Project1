from game import Game
from coord import Coord, CoordPair
import copy

def generateMoves(game: Game) -> list[Game]:
    nextPlayer = game.next_player
    nextMoves = []

    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            curUnit = game.board[i][j]
            if curUnit.player == nextPlayer:
                srcCoord = Coord(i, j)
                for dstCoord in srcCoord.iter_adjacent():
                    nextMoves.append(copy.deepcopy(game).perform_move(CoordPair(srcCoord, dstCoord)))
                nextMoves.append(copy.deepcopy(game).perform_move(CoordPair(srcCoord, srcCoord)))

    return nextMoves