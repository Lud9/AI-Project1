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
                        nextState = copy.deepcopy(game)
                        (success, result) = nextState.perform_move(CoordPair(srcCoord, dstCoord))
                        if success:
                            nextState.next_turn()
                            nextStates.append(nextState)
                selfDestructState = copy.deepcopy(game)
                (success, result) = selfDestructState.perform_move(CoordPair(srcCoord, srcCoord))
                if success:
                    selfDestructState.next_turn()
                    nextStates.append(selfDestructState)
    return nextStates
