import pygame as pyg
import GameParameters as par
import numpy as np

class GameState:
    def __init__(self):
        self.game_running = True
        self.board_occupation_matrix = np.zeros((par.GRID_NR_OF_ROWS, par.GRID_NR_OF_COLS))
        self.keys_pressed = pyg.key.get_pressed()
        self.keys_pressed_prev = self.keys_pressed
        self.clock = pyg.time.Clock()
        # event to detect if tile needs to fall by one square, triggered at regular time intervals
        # event ID = 24 (up to 32, but first 23 are used by pygame already)
        self.gravity_tick_ev = pyg.USEREVENT + 0
        pyg.time.set_timer(self.gravity_tick_ev, par.FALL_TIME_INTERVAL_ms) 

    def lateral_key_released(self) -> bool:
        if self.keys_pressed_prev[pyg.K_LEFT] or self.keys_pressed_prev[pyg.K_RIGHT] and \
                ((not self.keys_pressed[pyg.K_LEFT]) and
                (not self.keys_pressed[pyg.K_RIGHT])):
            return True
        else:
            return False
    
    def rotation_key_released(self) -> bool:
        if self.keys_pressed_prev[pyg.K_SPACE] and (not self.keys_pressed[pyg.K_SPACE]):
            return True
        else:
            return False