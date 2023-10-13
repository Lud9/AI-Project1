from game import Game
from coord import Coord, CoordPair
import copy


def generateStates(game: Game) -> list[Game]:
    nextPlayer = game.next_player
    nextStates = []

    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            curUnit = game.board[i][j]
            if curUnit is not None and curUnit.player == nextPlayer:
                srcCoord = Coord(i, j)
                for dstCoord in srcCoord.iter_adjacent():
                    if game.is_valid_coord(dstCoord):
                        nextMove = copy.deepcopy(game)
                        (success, result) = nextMove.perform_move(CoordPair(srcCoord, dstCoord))
                        if success:
                            nextStates.append(nextMove)
                selfDestructMove = copy.deepcopy(game)
                selfDestructMove.perform_move(CoordPair(srcCoord, srcCoord))
                nextStates.append(selfDestructMove)
    return nextStates
