import sys, os

# Handle PyInstaller vs normal execution
BASE_PATH = (
    sys._MEIPASS
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, os.path.join(BASE_PATH, "src"))

import parameters as par
from interface import *


def main() -> None:
    """Main function to run the game loop.
    
    """

    game_interface = GameInterface()
    while game_interface.state.game_running:
        game_interface.process_events_and_inputs()
        game_interface.update()
        game_interface.draw_frame()
        # waits until the desired fps is reached
        game_interface.state.get_clock().tick(par.TARGET_FPS)          
    pyg.quit() 
    
if __name__ == "__main__":
    main()