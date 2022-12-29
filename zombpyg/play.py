import argparse
from threading import Thread
import pygame
from zombpyg.agent import AgentActions
from zombpyg.game import Game

def render_game_in_thread(game):
    termination = False
    while not termination:
        game.draw()
        if pygame.event.peek(): 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_9:
                        game.increase_fps()
                    elif event.key == pygame.K_0:
                        game.decrease_fps()    
                    elif event.key == pygame.K_w:
                        _, _, termination = game.play_action(
                            AgentActions.get_forward_move_action_id()
                        )
                    elif event.key == pygame.K_d:
                        _, _, termination = game.play_action(
                            AgentActions.get_right_move_action_id()
                        )
                    elif event.key == pygame.K_s:
                        _, _, termination = game.play_action(
                            AgentActions.get_backward_move_action_id()
                        )
                    elif event.key == pygame.K_a:
                        _, _, termination = game.play_action(
                            AgentActions.get_left_move_action_id()
                        )
                    elif event.key == pygame.K_RIGHT:
                        _, _, termination = game.play_action(
                            AgentActions.get_smallest_right_rotation_action_id()
                        )
                    elif event.key == pygame.K_LEFT:
                        _, _, termination = game.play_action(
                            AgentActions.get_smallest_left_rotation_action_id()
                        )
                    elif event.key == pygame.K_SPACE:
                        _, _, termination = game.play_action(
                            AgentActions.get_use_weapon_action_id()
                        )
                    elif event.key == pygame.K_h:
                        _, _, termination = game.play_action(
                            AgentActions.get_self_heal_action_id()
                        )
                    elif event.key == pygame.K_g:
                        _, _, termination = game.play_action(
                            AgentActions.get_heal_player_action_id()
                        )
        else:
            # No action
            _, _, termination = game.play_action(
                AgentActions.get_no_action_id()
            )
        print(f"Total Reward: {game.get_total_reward()}")

def main(): 
    parser = argparse.ArgumentParser(description="zombpyg")
    parser.add_argument("-r", "--rules", dest="rules_id", metavar="RULES_ID", type=str, nargs=1, required=False, help="The rules id")
    parser.add_argument("-z", dest="initial_zombies", metavar="NUMBER", type=int, nargs=1, required=False, default=[5], help="The initial amount of zombies")
    parser.add_argument("-n", dest="minimum_zombies", metavar="NUMBER", type=int, nargs=1, required=False, default=[0], help="The minimum amount of zombies at all times")
    parser.add_argument("--players", dest="player_specs", metavar="PLAYER_TYPE:WEAPON:COUNT,...", type=str, nargs=1, required=False, help="The players specified as a comma-separated list of player_id:weapon_id:count")
    parser.add_argument("--verbose", dest="verbose", default=False, action="store_true")

    args = parser.parse_args()
    rules_id = args.rules_id[0] if args.rules_id is not None else "survival"
    initial_zombies = args.initial_zombies[0]
    minimum_zombies = args.minimum_zombies[0]
    player_specs = args.player_specs[0] if args.player_specs is not None else ""
    verbose = args.verbose
    
    pygame.init()
    pygame.key.set_repeat(100, int(1000/50))
    DISPLAYSURF = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption('zombpyg')
    game = Game(
        640, 480,
        DISPLAYSURF,
        initial_zombies=initial_zombies, minimum_zombies=minimum_zombies,
        rules_id=rules_id,
        player_specs=player_specs,
        verbose=verbose,
    )
    t = Thread(target=lambda: render_game_in_thread(game))
    t.start()
    game.reset()
    t.join()

if __name__ == "__main__":
    main()
