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
            
    
def update_scene():
    # color background such that older objects do not appear
    game_window.fill(BLACK)
    
    # draw rectangle
    pyg.draw.rect(game_window, RED, (x, y, rect_width, rect_height))
    pyg.display.update()
    
    
# define some parameters
fps = 60
ms_per_frame =int((1/fps)*1000)
delta_s = 1
RED = (255, 0, 0)
BLACK = (0, 0, 0)

game_window_width = 1000
game_window_height = 1000

# initial rectangle position (top left corner)
x = game_window_width/2
y = game_window_height/2

# rectangle dimensions
rect_width = 10
rect_height = 100

pyg.init()
game_window = pyg.display.set_mode((game_window_width, game_window_height))
pyg.display.set_caption("Tetris")

game_running = True    
while game_running:
    # wait to display next frame
    pyg.time.delay(ms_per_frame)
    
    # pressing the "X" button terminates the application
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            game_running = False
            
    process_player_inputs()
    update_scene()
            
pyg.quit()