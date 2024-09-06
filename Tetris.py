import pygame as pyg

def process_player_inputs():
    global x, y
    keys_pressed = pyg.key.get_pressed()
    
    if keys_pressed[pyg.K_LEFT]:
        if not keys_pressed[pyg.K_RIGHT]:
            x -= delta_s
            
    if keys_pressed[pyg.K_RIGHT]:
        if not keys_pressed[pyg.K_LEFT]:
            x += delta_s
            
    if keys_pressed[pyg.K_UP]:
        if not keys_pressed[pyg.K_DOWN]:
            y -= delta_s

    if keys_pressed[pyg.K_DOWN]:
        if not keys_pressed[pyg.K_UP]:
            y += delta_s            
            
def draw_grid():
    for column in range(50, 50+GRID_ELEM_SIZE*15, GRID_ELEM_SIZE):
        for row in range(50, 50+GRID_ELEM_SIZE*15, GRID_ELEM_SIZE):
            grid_element = pyg.Rect(row, column, GRID_ELEM_SIZE, GRID_ELEM_SIZE)
            pyg.draw.rect(game_window, BLACK, grid_element, 1)

            
    
def update_scene():
    # color background such that older objects do not appear
    game_window.blit(BACKGROUND, (0, 0))
    
    draw_grid()
    
    # draw rectangle
    pyg.draw.rect(game_window, RED, (x, y, GRID_ELEM_SIZE, GRID_ELEM_SIZE))
    # After calling the drawing functions to make the display Surface object look the way you want, you must call this to make the display Surface actually appear on the user’s monitor.
    pyg.display.update()
    
    
# define some parameters
FPS = 60
delta_s = 1
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID_ELEM_SIZE = 20

game_window_width = 1700
game_window_height = 1000

pyg.init()
game_window = pyg.display.set_mode((game_window_width, game_window_height))
pyg.display.set_caption("Tetris")

BACKGROUND = pyg.image.load('assets/bg.jpg')

clock = pyg.time.Clock()

# initial rectangle position (top left corner)
x = game_window.get_width()/2
y = game_window.get_height()/2

game_running = True    
while game_running:
    # pressing the "X" button terminates the application
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            game_running = False
            
    process_player_inputs()
    update_scene()
    
    # limits game's fps (waits) and returns the ms count since the last call
    clock.tick(FPS)
            
pyg.quit()