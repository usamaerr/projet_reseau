import configparser
from random import *
from time import sleep

import pygame
import pygame.font

from grid import Grid

pygame.init()
pygame.mixer.init()
# collision_sound = pygame.mixer.Sound("asset\Cartoon Accent.mp3")
# start_sound = pygame.mixer.Sound("asset\Cartoon Accent.mp3")
# newblob = pygame.mixer.Sound("asset/new_blob.mp3")
config = configparser.ConfigParser()
config.read('config.ini')

# Font settings
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 20)

# Window dimensions
screen_width = config.getint('Dimensions', 'WIDTH')
screen_height = config.getint('Dimensions', 'HEIGHT')
g_nb_bob = config.getint('Dimensions', 'nb_bob')
g_nb_food = config.getint('Dimensions', 'nb_food')
energie = config.getint('Dimensions', 'energie')
mut_rate = config.getfloat('Dimensions', 'mut_rate')

# Initialize the window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulation de Blobs")

def calculate_cell_dimensions(grid_height, grid_width, num_rows, num_columns):
    # Calculate cell height and width
    cell_height = grid_height / num_rows
    cell_width = grid_width / num_columns
    return cell_height, cell_width

cell_height, cell_width = calculate_cell_dimensions(config.getint('Dimensions', 'HEIGHT'), config.getint('Dimensions', 'WIDTH'), 20, 20)

def load_blob_images():
    mauve_blob_image = pygame.image.load("asset/blob_mauve.png")
    bleu_blob_image = pygame.image.load("asset/blob_bleu.png")
    vert_blob_image = pygame.image.load("asset/blob-161097_1280.png")

    return mauve_blob_image, bleu_blob_image, vert_blob_image

# Load blob images
mauve_blob_image, bleu_blob_image, vert_blob_image = load_blob_images()

# Load food image
food_image = pygame.image.load("asset/crab_meat.png")
food_image = pygame.transform.scale(food_image, (cell_width, cell_width))

def draw_grid(screen, rows, cols):
    cell_size = screen_width // cols
    for i in range(1, cols):
        pygame.draw.line(screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, screen_height))
    for j in range(1, rows):
        pygame.draw.line(screen, (0, 0, 0), (0, j * cell_size), (screen_width, j * cell_size))

def display_grid(grid, screen):
    cell_size = screen_width // grid.M

    # Clear the grid
    screen.fill((255, 255, 255))

    # Draw the grid
    draw_grid(screen, grid.N, grid.M)

    for (x, y) in list(grid.dict_bob.keys()):
        bobs_at_location = grid.dict_bob[(x, y)]
        blob_image = None # Provide a default value
        if bobs_at_location:
            bob = bobs_at_location[0]  # Access the first blob if there is one
            if 0 <= bob.energy <= 66:
                blob_image = mauve_blob_image
            elif 66 <= bob.energy <= 136:
                blob_image = bleu_blob_image
            elif 136 <= bob.energy <= 200:
                blob_image = vert_blob_image

            if blob_image is not None:
                blob_image = pygame.transform.scale(blob_image, (cell_width, cell_width))
                screen.blit(blob_image, (x * cell_size, y * cell_size))

                # Render and display energy value above each bob
                energy_text = font2.render(f'{bob.get_energy()}', True, (0, 0, 0))
                screen.blit(energy_text, (x * cell_size + cell_size // 2 - energy_text.get_width() // 2,
                                        y * cell_size - 10))

    # Draw the food
    for (x, y) in grid.dict_food.keys():
        food_energy_text = font2.render(f'{grid.dict_food[(x, y)]}', True, (0, 0, 0))
        screen.blit(food_image, (x * cell_size, y * cell_size))
        screen.blit(food_energy_text, (x * cell_size + cell_size // 2 - food_energy_text.get_width() // 2,
                                       y * cell_size - 10))

# Game initialization
running = True
paused = False
def init(grid,subsurface):
    grid = Grid(20, 20,g_nb_bob,g_nb_food,mut_rate,energie)  # 20 columns, 20 rows
    grid.create_grid()
    grid.create_all_bob()
    grid.create_all_food()

    screen = subsurface 

    screen.fill((255, 255, 255))  # Fill the screen with white
    draw_grid(screen, grid.N, grid.M)  # Draw the grid
    pygame.display.flip()  # Refresh the screen to display the grid before playing the sound
    # start_sound.play()  # Play the sound at the beginning of the game

    return grid , subsurface

grid = Grid(0, 0)
grid, subsurface = init(grid,screen.subsurface(pygame.Rect(0, 0, screen_width, screen_height)))
tick = config.getint('Dimensions', 'tick')
tick_count = 0

# Main loop
while running and tick_count <= tick:  # Reduce the number of iterations
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Press 'P' to toggle pause
                paused = not paused
            elif event.key == pygame.K_m:  # Press 'M' to return to the menu
                running = False  # Set running to False to exit the loop
    if not paused:
        grid.action_bob_speed()
        
       
        display_grid(grid, screen)

        # Render and display the tick in the top-right corner
        text = font.render(f'Tick: {grid.tick}', True, (0, 0, 0))  # Black color
        screen.blit(text, (screen_width - text.get_width() - 10, 10))

        day_text = font.render(f'Day: {grid.day}', True, (0, 0, 0))  # Black color
        screen.blit(day_text, (10, 10))
        # Refresh the screen
        pygame.display.flip()
    
    # Control the frame rate
    sleep(0.5)
    pygame.time.Clock().tick(30)
    # tick_count += 1

pygame.quit()
