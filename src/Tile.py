import GameParameters as par
import pygame as pyg

class Tile:
    def __init__(self, type) -> None:
        self.type = type
        self.vertical_movement_allowed = True
        self.lateral_movement_allowed = True
        self.rotation_allowed = True
        self.is_falling = False
        self.bottom_reached = False
        self.configuration_idx = 0
        self.position = pyg.Vector2(par.GRID_TLC_x + par.GRID_ELEM_SIZE * int(par.GRID_NR_OF_COLS / 2),
                                    par.GRID_TLC_y)
        self.configuration_matrix = par.TILE_SHAPES[self.type][self.configuration_idx]
    
    def rotate(self) -> None:
        self.configuration_idx = (self.configuration_idx + 1) % par.TILE_CONFIG_IDX_MAX
        self.configuration_matrix = par.TILE_SHAPES[self.type][self.configuration_idx]
    
    def update_position(self, lateral_key_released, rotation_key_released):
        keys_pressed = pyg.key.get_pressed()
        
        # Check if bottom was reached
        config_mat_bot_filled = False
        config_mat_rows = len(self.configuration_matrix[self.configuration_idx])
        for idx in range (0, config_mat_rows):
            if self.configuration_matrix[self.configuration_idx][idx] == 1:
                config_mat_bot_filled = True
                break
                
        if ((self.position.y + config_mat_rows * par.GRID_ELEM_SIZE == par.GRID_TLC_y + par.GRID_ELEM_SIZE * par.GRID_NR_OF_ROWS) and
                config_mat_bot_filled == True):
                    self.bottom_reached = True

        # Check if a lateral movement key was released
        if ((not lateral_key_released) and (not keys_pressed[pyg.K_LEFT])
                and (not keys_pressed[pyg.K_RIGHT])):
            lateral_key_released = True
            
        # Check if rotation key was released
        if ((not rotation_key_released) and (not keys_pressed[pyg.K_SPACE])):
            rotation_key_released = True        
        
        if (keys_pressed[pyg.K_LEFT] and (not keys_pressed[pyg.K_RIGHT])
                and self.position.x > par.GRID_TLC_x and lateral_key_released):
            self.position.x -= par.GRID_ELEM_SIZE
            lateral_key_released = False
                
        if (keys_pressed[pyg.K_RIGHT] and (not keys_pressed[pyg.K_LEFT])
                and self.position.x < par.GRID_TLC_x + par.GRID_ELEM_SIZE * (par.GRID_NR_OF_COLS - 1)
                and lateral_key_released):
            self.position.x += par.GRID_ELEM_SIZE
            lateral_key_released = False
        
        if (keys_pressed[pyg.K_SPACE] and self.rotation_allowed and rotation_key_released):
            self.rotate()
            rotation_key_released = False
            
        if self.is_falling and (not self.bottom_reached):
            self.position.y += par.GRID_ELEM_SIZE
            self.is_falling = False
            
        return lateral_key_released, rotation_key_released