import sys, os
sys.path.append(os.path.join(sys.path[0], 'src'))
import parameters as par
from interface import *

def main():
    game_interface = GameInterface()
    while game_interface.state.game_running:
        game_interface.process_events_and_inputs()
        if not game_interface.state.game_paused:
            game_interface.update()
        game_interface.draw_scene()
        if game_interface.state.game_paused:
            game_interface.pause_menu()
        # waits until the desired fps is reached
        game_interface.state.clock.tick(par.TARGET_FPS)          
    pyg.quit() 
    
if __name__ == "__main__":
    main()