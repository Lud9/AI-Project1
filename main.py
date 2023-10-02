import os
import argparse
from game import Game, GameType, Player, CoordPair,Options
    
def main():
    #Command line example:  python main.py --max_depth 2 --max_time 5 --max_turns 2
    # parse command line arguments
    parser = argparse.ArgumentParser( prog='ai_wargame', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--max_depth', type=int, help='maximum search depth')
    parser.add_argument('--max_time', type=float, help='maximum search time')
    parser.add_argument('--game_type', type=str, default="manual", help='game type: auto|attacker|defender|manual')
    parser.add_argument('--broker', type=str, help='play via a game broker')
    
    #########The maximum number of turns to declare the end of the game 
    parser.add_argument('--max_turns', type=int, help='number of turns before game ends') 
    parser.add_argument('--alpha_beta', type=bool, help='A Boolean to force the use of either minimax (FALSE) or alpha-beta (TRUE)')
    
    args = parser.parse_args()

    
    # parse the game type
    if args.game_type == "attacker":
        game_type = GameType.AttackerVsComp
    elif args.game_type == "defender":
        game_type = GameType.CompVsDefender
    elif args.game_type == "manual":
        game_type = GameType.AttackerVsDefender
    else:
        game_type = GameType.CompVsComp

    # set up game options
    options = Options(game_type=game_type)

    # override class defaults via command line options
    if args.max_depth is not None:
        options.max_depth = args.max_depth
    if args.max_time is not None:
        options.max_time = args.max_time
    if args.broker is not None:
        options.broker = args.broker
    
    ########## override 
    if args.max_turns is not None:
        options.max_turns = args.max_turns
    if args.alpha_beta is not None:
        options.alpha_beta = args.alpha_beta

    # create a new game
    game = Game(options=options)

    
############### Function to generate output file
    filename = f"gameTrace-{options.alpha_beta}-{options.max_time}-{options.max_turns}.txt"
    
    def make_unique_filename(filename):
            base, ext = os.path.splitext(filename)
            counter = 1
            new_filename = filename
            while os.path.exists(new_filename):
                new_filename = f"{base}({counter}){ext}"
                counter += 1
            return new_filename
    
    filename = make_unique_filename(filename)

    def generate_output_file(coords: CoordPair = None):
        with open(filename, 'a') as file:
            try:
                if os.path.exists(filename):
                    if (os.path.getsize(filename)<= 0):
                        file.write(f"Value of the timeout in seconds: {options.max_time}\n")
                        file.write(f"The maximum number of turns: {options.max_turns}\n")
                        if ('Comp' in {game_type}):
                            file.write(f"The alpha-beta is {options.alpha_beta}\n")
                            if {game_type}.find('Comp')< {game_type}.find('r'):
                                file.write("Player 1 is AI & Player 2 is H\n")
                            else:
                                file.write("Player 1 is H & Player 2 is AI\n")
                            #file.write(f"{heuristic_name}")##################### Heuristic name TBD in ASS2
                        else:
                            file.write("Player 1 is H & Player 2 is H\n\n")
                file.write(f"{game}\n")
                if (coords is not None):
                    file.write(f"Action taken: {coords.src}-{coords.dst} \n\n\n")
                #if ('Comp' in strg): ##################### TBD in Ass2
                    # file.write(f"Time for this action: {}")
                    # file.write(f"Heuristic score: {}\n")
                    # file.write(f"Cummulative evals: {}\n Cummulative evals by depth: {}\n Cummulative % evals per depth: {}\n Average branching factor: {}\n")
                if game.has_winner() is not None:
                    file.write(f"{game.has_winner().name} wins in {game.turns_played} turns\n")
            except Exception as e:
                print(e)

    # the main game loop
    mv = None
    while True:
        print()
        print(game)
        generate_output_file(mv)
        winner = game.has_winner()
        if winner is not None:
            print(f"{winner.name} wins!")
            break
        if game.options.game_type == GameType.AttackerVsDefender:
            mv = game.human_turn()
        elif game.options.game_type == GameType.AttackerVsComp and game.next_player == Player.Attacker:
            mv = game.human_turn()
        elif game.options.game_type == GameType.CompVsDefender and game.next_player == Player.Defender:
            mv = game.human_turn()
        else:
            player = game.next_player
            move = game.computer_turn()            
            if move is not None:
                game.post_move_to_broker(move)
            else:
                print("Computer doesn't know what to do!!!")
                exit(1)        
if __name__ == '__main__':
    main()  
