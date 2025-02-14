import argparse
import pygame
from zombpyg.agent import AgentActions
from zombpyg.game import Game

def render_game(game):
    termination = False
    while not termination:
        game.draw()
        if pygame.event.peek(): 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    done = False
                    truncated = False

                    if event.key == pygame.K_9:
                        game.increase_fps()
                    elif event.key == pygame.K_0:
                        game.decrease_fps()    
                    elif event.key == pygame.K_w:
                        _, _, done, truncated = game.play_action(
                            AgentActions.get_forward_move_action_id()
                        )
                    elif event.key == pygame.K_d:
                        _, _, done, truncated = game.play_action(
                            AgentActions.get_right_move_action_id()
                        )
                    elif event.key == pygame.K_s:
                        _, _, done, truncated = game.play_action(
                            AgentActions.get_backward_move_action_id()
                        )
                    elif event.key == pygame.K_a:
                        _, _, done, truncated = game.play_action(
                            AgentActions.get_left_move_action_id()
                        )
                    elif event.key == pygame.K_RIGHT:
                        _, _, done, truncated = game.play_action(
                            AgentActions.get_smallest_right_rotation_action_id()
                        )
                    elif event.key == pygame.K_LEFT:
                        _, _, done, truncated = game.play_action(
                            AgentActions.get_smallest_left_rotation_action_id()
                        )
                    elif event.key == pygame.K_SPACE:
                        _, _, done, truncated = game.play_action(
                            AgentActions.get_use_weapon_action_id()
                        )
                    elif event.key == pygame.K_h:
                        _, _, done, truncated = game.play_action(
                            AgentActions.get_self_heal_action_id()
                        )
                    elif event.key == pygame.K_g:
                        _, _, done, truncated = game.play_action(
                            AgentActions.get_heal_player_action_id()
                        )
                    termination = done or truncated
        else:
            # No action
            _, _, done, truncated = game.play_action(
                AgentActions.get_no_action_id()
            )
            termination = done or truncated
        print(f"Total Reward: {game.agent_rewards[0].get_total_reward()}")

def main(): 
    parser = argparse.ArgumentParser(description="zombpyg")
    parser.add_argument("-r", "--rules", dest="rules_id", metavar="RULES_ID", type=str, nargs=1, required=False, help="The rules id")
    parser.add_argument("-m", "--map", dest="map_id", metavar="MAP_ID", type=str, nargs=1, required=False, help="The map id")
    parser.add_argument("-z", dest="initial_zombies", metavar="NUMBER", type=int, nargs=1, required=False, default=[5], help="The initial amount of zombies")
    parser.add_argument("-n", dest="minimum_zombies", metavar="NUMBER", type=int, nargs=1, required=False, default=[0], help="The minimum amount of zombies at all times")
    parser.add_argument("--players", dest="player_specs", metavar="PLAYER_TYPE:WEAPON:COUNT,...", type=str, nargs=1, required=False, help="The players specified as a comma-separated list of player_id:weapon_id:count")
    parser.add_argument("--verbose", dest="verbose", default=False, action="store_true")

    args = parser.parse_args()
    rules_id = args.rules_id[0] if args.rules_id is not None else "survival"
    map_id = args.map_id[0] if args.map_id is not None else "demo"
    initial_zombies = args.initial_zombies[0]
    minimum_zombies = args.minimum_zombies[0]
    player_specs = args.player_specs[0] if args.player_specs is not None else ""
    verbose = args.verbose
    
    pygame.init()
    pygame.key.set_repeat(100, int(1000/50))
    game = Game(
        640, 480,
        map_id=map_id,
        initial_zombies=initial_zombies, minimum_zombies=minimum_zombies,
        rules_id=rules_id,
        player_specs=player_specs,
        enable_rendering=True,
        friendly_fire_guard=True,
        verbose=verbose,
    )
    game.reset()
    render_game(game)

if __name__ == "__main__":
    main()
