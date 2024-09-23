import GameParameters as par
import pygame as pyg

class Tile:
    def __init__(self, type) -> None:
        self.type = type
        self.vertical_movement_allowed = True
        self.lateral_movement_allowed = True
        self.rotation_allowed = True
        self.is_falling = False
        self.configuration_idx = 0
        self.position = pyg.Vector2(par.GRID_TLC_x + par.GRID_ELEM_SIZE * int(par.GRID_NR_OF_COLS / 2),
                                    par.GRID_TLC_y)
        self.configuration_matrix = par.TILE_SHAPES[self.type][self.configuration_idx]
    
    def rotate(self) -> None:
        self.configuration_idx = (self.configuration_idx + 1) % par.TILE_CONFIG_IDX_MAX
        self.configuration_matrix = par.TILE_SHAPES[self.type][self.configuration_idx]
        
    def get_lowest_filled_height(self):
        lowest_filled_y = self.position.y
        is_found = False
        for inv_row in range(0, len(self.configuration_matrix)):
            if is_found:
                break
            for col in range(0, len(self.configuration_matrix)):
                if self.configuration_matrix[(len(self.configuration_matrix) - 1) - inv_row][col] == 1:
                    lowest_filled_y += ((len(self.configuration_matrix) - 1) - inv_row) * par.GRID_ELEM_SIZE
                    is_found = True
                    break
        # top left corner height
        return lowest_filled_y
    
    def get_furthest_pos_filled(self, direction):
        is_found = False
        furthest_filled_x = self.position.x
        for col in range(0, len(self.configuration_matrix)):
            if is_found:
                break
            for row in range(0, len(self.configuration_matrix)):
                if direction == 'LEFT':
                    if self.configuration_matrix[row][col] == 1:
                        furthest_filled_x += col * par.GRID_ELEM_SIZE
                        is_found = True
                        break
                elif direction == 'RIGHT':
                    # column index inverted
                    if self.configuration_matrix[row][(len(self.configuration_matrix) - 1) - col] == 1:
                        furthest_filled_x += ((len(self.configuration_matrix) - 1) - col) * par.GRID_ELEM_SIZE
                        is_found = True
                        break
                else:
                    pass # TODO throw error
                
        return furthest_filled_x
    
    def bottom_reached(self) -> bool:
        if self.get_lowest_filled_height() == par.GRID_TLC_y + par.GRID_ELEM_SIZE * (par.GRID_NR_OF_ROWS -1):
            self.rotation_allowed = False
            return True
        else:
            return False
        
    def update_position(self, game_state):
        # Check if lateral movement is prevented
        if game_state.lateral_movement_prevented and \
                ((not game_state.keys_pressed[pyg.K_LEFT]) and (not game_state.keys_pressed[pyg.K_RIGHT])):
            game_state.lateral_movement_prevented = False
            
        # Check if rotation is prevented
        if game_state.rotation_prevented and (not game_state.keys_pressed[pyg.K_SPACE]):
            game_state.rotation_prevented = False
        
        # Update left
        if (game_state.keys_pressed[pyg.K_LEFT] and (not game_state.keys_pressed[pyg.K_RIGHT])
                and (self.get_furthest_pos_filled('LEFT') > par.GRID_TLC_x)
                and (not game_state.lateral_movement_prevented)):
            self.position.x -= par.GRID_ELEM_SIZE
            game_state.lateral_movement_prevented = True
            
        # Update right 
        if (game_state.keys_pressed[pyg.K_RIGHT] and (not game_state.keys_pressed[pyg.K_LEFT])
                and (self.get_furthest_pos_filled('RIGHT') < par.GRID_TLC_x + par.GRID_ELEM_SIZE * (par.GRID_NR_OF_COLS - 1))
                and (not game_state.lateral_movement_prevented)):
            self.position.x += par.GRID_ELEM_SIZE
            game_state.lateral_movement_prevented = True
        
        if (game_state.keys_pressed[pyg.K_SPACE] and self.rotation_allowed and (not game_state.rotation_prevented)):
            self.rotate()
            game_state.rotation_prevented = True
            
        if self.is_falling and (not self.bottom_reached()):
            self.position.y += par.GRID_ELEM_SIZE
            self.is_falling = False