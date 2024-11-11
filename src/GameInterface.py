import pygame as pyg
import GameParameters as par
import pygame.freetype

class GameInterface:
    def __init__(self):
        pyg.init()
        self.game_window = pyg.display.set_mode((par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT))
        pyg.display.set_caption("Tetris")
        # https://www.freepik.com/icons/tetris Icon by Freepik
        self.icon = pyg.image.load('assets/tetris_icon.png')
        pyg.display.set_icon(self.icon)
        self.logo = pyg.image.load('assets/tetris_logo.png')
        self.text_font = pyg.freetype.SysFont(pyg.freetype.get_default_font(), par.FONT_SIZE)
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

    def draw_grid(self):
        # draw horizontal lines
        for row_idx in range(0, par.GRID_NR_OF_ROWS + 1):
            start_coords = (par.GRID_TLC_x, par.GRID_TLC_y + row_idx * par.GRID_ELEM_SIZE)
            end_coords = (par.GRID_TLC_x + par.GRID_NR_OF_COLS * par.GRID_ELEM_SIZE, 
                        par.GRID_TLC_y + row_idx * par.GRID_ELEM_SIZE)
            pyg.draw.line(surface=self.game_window, color=par.BLACK, 
                        start_pos=start_coords, end_pos=end_coords,
                        width=par.GRID_THICKNESS)
        # draw vertical lines    
        for col_idx in range(0, par.GRID_NR_OF_COLS + 1):
            start_coords = (par.GRID_TLC_x + col_idx * par.GRID_ELEM_SIZE, par.GRID_TLC_y)
            end_coords = (par.GRID_TLC_x + col_idx * par.GRID_ELEM_SIZE, 
                        par.GRID_TLC_y + par.GRID_ELEM_SIZE * par.GRID_NR_OF_ROWS)
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
    
    def draw_scene(self, tile, game_state):
        # TODO: only draw tile and board each time not the entire thing
        # color background such that older objects do not appear
        self.game_window.fill(par.GREY)
        self.game_window.blit(self.logo, par.LOGO_POS)

        score_surface, _ = self.text_font.render(f'Score:  {game_state.score}', par.WHITE)
        level_surface, _ = self.text_font.render(f'Level:   {game_state.level}', par.WHITE)
        lines_surface, _ = self.text_font.render(f'Lines:   {game_state.lines}', par.WHITE)

        y_level = par.STATS_POS[1] + self.text_font.get_sized_height() + 10
        x_level = par.STATS_POS[0]
        y_lines = y_level + self.text_font.get_sized_height() + 10
        x_lines = x_level

        self.game_window.blit(score_surface, par.STATS_POS)
        self.game_window.blit(level_surface, (x_level, y_level))
        self.game_window.blit(lines_surface, (x_lines, y_lines))
        
        self.draw_grid()
        self.draw_board(game_state)
        self.draw_tile(tile) 
        # After calling the drawing functions to make the display Surface object look the way you want, you must call this to make the display Surface actually appear on the user’s monitor.
        pyg.display.update()