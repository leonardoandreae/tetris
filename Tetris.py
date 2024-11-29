import sys, os
sys.path.append(os.path.join(sys.path[0], 'src'))
import GameParameters as par
from Tile import *
from GameState import *
from GameInterface import *

def main():
    game_interface = GameInterface()
    game_state = GameState()
    tile = Tile(game_state)
    
    while game_state.game_running:
        game_interface.event_handler(tile, game_state)
        game_state.get_current_keys()
        tile.update_position(game_state, game_interface)
        game_state.delete_complete_rows(game_interface)
        game_interface.draw_scene(tile, game_state)
        game_state.game_over_check()
        # waits until the desired fps is reached
        game_state.clock.tick(par.FPS)          
    pyg.quit() 
    
if __name__ == "__main__":
    main()