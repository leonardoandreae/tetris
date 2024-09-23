import pygame as pyg
import GameParameters as par
import numpy as np

class GameState:
    def __init__(self):
        self.game_running = True
        self.board_occupation_matrix = np.zeros((par.GRID_NR_OF_ROWS, par.GRID_NR_OF_COLS))
        self.get_current_keys()
        self.update_prev_keys()
        self.lateral_movement_prevented = False
        self.rotation_prevented = False
        self.clock = pyg.time.Clock()
        # event to detect if tile needs to fall by one square, triggered at regular time intervals
        # event ID = 24 (up to 32, but first 23 are used by pygame already)
        self.gravity_tick_ev = pyg.USEREVENT + 0
        pyg.time.set_timer(self.gravity_tick_ev, par.FALL_TIME_INTERVAL_ms) 
        
    def get_current_keys(self) -> None:
        self.keys_pressed = pyg.key.get_pressed()
        
    def update_prev_keys(self) -> None:
        self.keys_pressed_prev = self.keys_pressed
    
    def lateral_movement_check(self):
        if self.lateral_movement_prevented and \
                ((not self.keys_pressed[pyg.K_LEFT]) and (not self.keys_pressed[pyg.K_RIGHT])):
            self.lateral_movement_prevented = False
        
    def rotation_check(self):
        if self.rotation_prevented and (not self.keys_pressed[pyg.K_SPACE]):
            self.rotation_prevented = False
        
    def update_occupation_matrix(self) -> None:
        pass
        
    
