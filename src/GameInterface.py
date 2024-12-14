import pygame as pyg
import GameParameters as par
import pygame.freetype

class GameInterface:
    def __init__(self):
        pyg.init()
        self.game_window = pyg.display.set_mode((par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT))
        pyg.display.set_caption("Tetris")
        self.icon = pyg.image.load('assets/tetris_icon.png') # https://www.freepik.com/icons/tetris Icon by Freepik
        pyg.display.set_icon(self.icon)
        self.logo = pyg.image.load('assets/tetris_logo.png')
        self.text_font_1 = pyg.freetype.SysFont(pyg.freetype.get_default_font(), par.FONT_SIZE_1)
        self.text_font_2 = pyg.freetype.SysFont(pyg.freetype.get_default_font(), par.FONT_SIZE_2)
        pyg.mixer.music.load('assets/tetris-theme.mp3')
        self.rotation_sfx = pyg.mixer.Sound('assets/rotation.mp3')
        self.single_sfx = pyg.mixer.Sound('assets/single.mp3')
        self.double_sfx = pyg.mixer.Sound('assets/double.mp3')
        self.triple_sfx = pyg.mixer.Sound('assets/triple.mp3')
        self.quadruple_sfx = pyg.mixer.Sound('assets/quadruple.mp3')
        self.play_main_theme()
        
    def play_main_theme(self):
        pyg.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
        pyg.mixer.music.set_volume(par.MUSIC_VOLUME)

    def event_handler(self, tile, game_state):
        for event in pyg.event.get():
            # pressing the "X" button terminates the application
            if event.type == pyg.QUIT:
                game_state.game_running = False
            if event.type == game_state.gravity_tick_ev:
                tile.is_falling = True
            if event.type == game_state.downwards_drop_ev:
                tile.can_drop = True

    def compute_smallest_drop_distance(self, tile, game_state):
        drop_distances = [] # unit = number of cells
        for col in range(0, par.TILE_CONFIG_IDX_MAX):
            d_up = 0
            d_down = 0
            for row in range(par.TILE_CONFIG_IDX_MAX - 1, -1, -1):
                if tile.configuration_matrix[row][col] == 1:
                    row_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + par.TILE_CONFIG_IDX_MAX
                    col_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col
                    while(row_ < par.GRID_NR_OF_ROWS):
                        print(f'col = {col_}')
                        if game_state.board_occupation_matrix[row_][col_] == None:
                            d_down += 1
                            row_ += 1
                        else:
                            break
                    drop_distances.append(d_up + d_down)
                    break
                else:
                    d_up += 1
        return min(drop_distances)

    def draw_grid(self, nr_of_rows, nr_of_cols, TLC_coords):
        # draw horizontal lines
        for row_idx in range(0, nr_of_rows + 1):
            start_coords = (TLC_coords.x, TLC_coords.y + row_idx * par.GRID_ELEM_SIZE)
            end_coords = (TLC_coords.x + nr_of_cols * par.GRID_ELEM_SIZE, 
                        TLC_coords.y + row_idx * par.GRID_ELEM_SIZE)
            pyg.draw.line(surface=self.game_window, color=par.BLACK, 
                        start_pos=start_coords, end_pos=end_coords,
                        width=par.GRID_THICKNESS)
        # draw vertical lines    
        for col_idx in range(0, nr_of_cols + 1):
            start_coords = (TLC_coords.x + col_idx * par.GRID_ELEM_SIZE, TLC_coords.y)
            end_coords = (TLC_coords.x + col_idx * par.GRID_ELEM_SIZE, 
                         TLC_coords.y + par.GRID_ELEM_SIZE * nr_of_rows)
            pyg.draw.line(surface=self.game_window, color=par.BLACK, 
                        start_pos=start_coords, end_pos=end_coords,
                        width=par.GRID_THICKNESS)

    def draw_block_with_borders(self, TLC_x, TLC_y, size, color, border_color):
        block = pyg.Rect(TLC_x, TLC_y, size, size)
        pyg.draw.rect(self.game_window, color, block)
        top_left = (TLC_x, TLC_y) 
        down_left = (top_left[0], top_left[1] + size)
        down_right = (down_left[0] + size, down_left[1])
        top_right = (down_right[0], down_right[1] - size)
        pyg.draw.lines(surface=self.game_window, color=border_color, closed=True,
                    points=[top_left, down_left, down_right, top_right],
                    width=par.BLOCK_BORDER_THICKNESS)

    def draw_board(self, game_state):
        for row in range (0, par.GRID_NR_OF_ROWS):
            for col in range (0, par.GRID_NR_OF_COLS):
                if game_state.board_occupation_matrix[row][col] != None:
                    self.draw_block_with_borders(par.GRID_TLC_x + col * par.GRID_ELEM_SIZE,
                                                 par.GRID_TLC_y + row * par.GRID_ELEM_SIZE,
                                                 par.GRID_ELEM_SIZE,
                                                 game_state.board_occupation_matrix[row][col],
                                                 par.WHITE)

    def draw_tile(self, tile):
        # draw tile with its border
        for col in range (0, par.TILE_CONFIG_IDX_MAX):
            for row in range (0, par.TILE_CONFIG_IDX_MAX):
                if tile.configuration_matrix[row][col] == 1:
                    self.draw_block_with_borders(tile.position.x + par.GRID_ELEM_SIZE * col,
                                                tile.position.y + par.GRID_ELEM_SIZE * row,
                                                par.GRID_ELEM_SIZE,
                                                par.TILE_COLORS[tile.type],
                                                par.WHITE)
                    
    # TODO unite this function with the one above                
    def draw_next_tile(self, tile_type):
        configuration_matrix = par.TILE_SHAPES[tile_type][0]
        for col in range (0, par.TILE_CONFIG_IDX_MAX):
            for row in range (0, par.TILE_CONFIG_IDX_MAX):
                if configuration_matrix[row][col] == 1:
                    self.draw_block_with_borders(par.NEXT_PIECE_GRID_POS.x + par.GRID_ELEM_SIZE * col,
                                                par.NEXT_PIECE_GRID_POS.y + par.GRID_ELEM_SIZE * row,
                                                par.GRID_ELEM_SIZE,
                                                par.TILE_COLORS[tile_type],
                                                par.WHITE)
                    
    def draw_dropped_tile_preview(self, tile, game_state):
        drop_distance = self.compute_smallest_drop_distance(tile, game_state)
        # draw tile outer border at drop distance
        for row in range (0, par.TILE_CONFIG_IDX_MAX):
            for col in range (0, par.TILE_CONFIG_IDX_MAX):
                if tile.configuration_matrix[row][col] == 1:                  
                    if row == 0 or tile.configuration_matrix[row - 1][col] == 0: # lazy or eval allows to avoid idx overflow (same below)
                        pyg.draw.line(self.game_window, 
                                        par.BLACK, 
                                        pyg.Vector2(tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)
                    if col == 0 or tile.configuration_matrix[row][col - 1] == 0:
                        pyg.draw.line(self.game_window, 
                                        par.BLACK, 
                                        pyg.Vector2(tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)                            
                    if row == par.TILE_CONFIG_IDX_MAX - 1 or tile.configuration_matrix[row + 1][col] == 0:
                        pyg.draw.line(self.game_window, 
                                        par.BLACK, 
                                        pyg.Vector2(tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        pyg.Vector2(tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)  
                    if col == par.TILE_CONFIG_IDX_MAX - 1 or tile.configuration_matrix[row][col + 1] == 0:
                        pyg.draw.line(self.game_window, 
                                        par.BLACK, 
                                        pyg.Vector2(tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)  

    def draw_scene(self, tile, game_state):
        # TODO: only draw tile and board each time not the entire thing
        # color background such that older objects do not appear
        self.game_window.fill(par.GREY)
        self.game_window.blit(self.logo, par.LOGO_POS)

        next_piece_text_surface, _ = self.text_font_2.render(f'Next Piece:', par.WHITE)
        score_text_surface, _ = self.text_font_1.render(f'Score:  {game_state.score}', par.WHITE)
        level_text_surface, _ = self.text_font_1.render(f'Level:   {game_state.level}', par.WHITE)
        lines_text_surface, _ = self.text_font_1.render(f'Lines:   {game_state.lines}', par.WHITE)

        # TODO: clean this up
        y_level = par.STATS_POS[1] + self.text_font_1.get_sized_height() + 10
        x_level = par.STATS_POS[0]
        y_lines = y_level + self.text_font_1.get_sized_height() + 10
        x_lines = x_level

        self.game_window.blit(score_text_surface, par.STATS_POS)
        self.game_window.blit(level_text_surface, (x_level, y_level))
        self.game_window.blit(lines_text_surface, (x_lines, y_lines))
        self.game_window.blit(next_piece_text_surface, par.NEXT_PIECE_TEXT_POS)
        
        self.draw_grid(4, 4, par.NEXT_PIECE_GRID_POS)
        self.draw_next_tile(tile.next_type)
        self.draw_grid(par.GRID_NR_OF_ROWS, par.GRID_NR_OF_COLS, pyg.Vector2(par.GRID_TLC_x, par.GRID_TLC_y))
        self.draw_board(game_state)
        self.draw_tile(tile)
        self.draw_dropped_tile_preview(tile, game_state)
        # After calling the drawing functions to make the display Surface object look the way you want, you must call this to make the display Surface actually appear on the user’s monitor.
        pyg.display.update()