import GameParameters as par
import pygame as pyg
import random

class Tile:
    def __init__(self, game_state) -> None:
        self.reset(game_state)

    def reset(self, game_state):
        self.type = self.get_next_type()
        self.vertical_movement_allowed = True
        self.lateral_movement_allowed = True
        self.rotation_allowed = False
        self.is_falling = False
        self.can_drop = False
        self.configuration_idx = 0
        self.position = self.get_initial_position()
        self.configuration_matrix = par.TILE_SHAPES[self.type][self.configuration_idx]
        # Check for contact and if occurred end the game
        game_state.contact_detection(self)
        if game_state.down_contact == True:
            game_state.game_running = False

    def get_next_type(self):
        tile_types = list(par.TILE_SHAPES.keys())
        idx = random.randint(0, len(tile_types) - 1)
        return tile_types[idx]
    
    def rotate(self, direction) -> None:
        if direction == 'CCW':
            self.configuration_idx = (self.configuration_idx + 1) % par.TILE_CONFIG_IDX_MAX
        elif direction == 'CW':
            self.configuration_idx = (self.configuration_idx - 1) % par.TILE_CONFIG_IDX_MAX
        else:
            pass
        self.configuration_matrix = par.TILE_SHAPES[self.type][self.configuration_idx]
        
    def get_initial_position(self):
        if self.type == "I" or self.type == "O":
            pos = pyg.Vector2(par.GRID_TLC_x + par.GRID_ELEM_SIZE * (int(par.GRID_NR_OF_COLS / 2) - 2),
                                    par.GRID_TLC_y - par.GRID_ELEM_SIZE)
        else:
            pos = pyg.Vector2(par.GRID_TLC_x + par.GRID_ELEM_SIZE * (int(par.GRID_NR_OF_COLS / 2) - 1),
                                    par.GRID_TLC_y - par.GRID_ELEM_SIZE)
        return pos
    
    def is_out_of_bounds(self, x, y):
        if (x < par.GRID_TLC_x or \
                x > par.GRID_TLC_x + (par.GRID_NR_OF_COLS - 1) * par.GRID_ELEM_SIZE or \
                y < par.GRID_TLC_y or \
                y > par.GRID_TLC_y + (par.GRID_NR_OF_ROWS - 1) * par.GRID_ELEM_SIZE):
            return True
        else:
            return False
    
    def is_position_permitted(self, game_state):
        for row in range(0, len(self.configuration_matrix)):
            for col in range(0, len(self.configuration_matrix)):
                # Check if the tile block is out of bounds
                block_pos_x = self.position.x + par.GRID_ELEM_SIZE * col
                block_pos_y = self.position.x + par.GRID_ELEM_SIZE * row
                if self.configuration_matrix[row][col] == 1 and self.is_out_of_bounds(block_pos_x, block_pos_y):
                    return False
                elif self.configuration_matrix[row][col] == 1 and (not self.is_out_of_bounds(block_pos_x, block_pos_y)):
                    # Check if the tile block is overlapping the board
                    row_ = int((self.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
                    col_ = int((self.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col
                    if game_state.board_occupation_matrix[row_][col_] != None:
                        return False
                else:
                    pass
        return True
                    
    def update_position(self, game_state, game_interface):
        # Check if lateral movement is disabled/enabled
        game_state.lateral_movement_check()
            
        # Check if rotation is disabled/enabled
        game_state.rotation_check()

        game_state.contact_detection(self)
        
        # Update left
        if (game_state.keys_pressed[par.LEFT] and (not game_state.keys_pressed[par.RIGHT])
                and (not game_state.left_contact)
                and (not game_state.lateral_movement_disabled)):
            self.position.x -= par.GRID_ELEM_SIZE
            game_state.lateral_movement_disabled = True
            
        # Update right
        if (game_state.keys_pressed[par.RIGHT] and (not game_state.keys_pressed[par.LEFT])
                and (not game_state.right_contact)
                and (not game_state.lateral_movement_disabled)):
            self.position.x += par.GRID_ELEM_SIZE
            game_state.lateral_movement_disabled = True
            
        # Update rotation state
        if (game_state.keys_pressed[par.ROTATE] and game_state.rotation_allowed_check(self, step=1) and (not game_state.rotation_disabled)):
            self.rotate('CCW')
            game_interface.rotation_sfx.play()
            game_state.rotation_disabled = True
        
        # Update vertical position
        if (not game_state.down_contact):
            if game_state.keys_pressed[par.DOWN]:
                self.position.y += self.can_drop * par.GRID_ELEM_SIZE
                if self.can_drop == True:
                    game_state.score += 1
                self.can_drop = False
            if (self.is_falling):
                self.position.y += par.GRID_ELEM_SIZE
                self.is_falling = False                
        else:
            game_state.update_occupation_matrix(self)
            self.reset(game_state)
              