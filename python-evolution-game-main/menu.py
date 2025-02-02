import pygame
import pygame_menu
from pygame.locals import *

import globals
from affichage_2_5D_isometric import get_config, get_config_from_settings
from game import start_game

pygame.init()
window_size = (900, 700)

themes = [('Default', 0), ('Christmas', 1), ('Halloween', 2), ('Pirate', 3), ('Space', 4)]

################# MENU FUNCTIONS ###################
def ask_player_name():
    def set_player_name(value):
        globals.player_name = value  # Mettre à jour le nom saisi

    def confirm_and_start():
        if globals.player_name.strip() == "":  # Vérifier si un nom a été saisi
            print("Veuillez saisir un nom valide.")
        else:
            print(f"Nom du joueur : {globals.player_name}")
            from affichage_2_5D_isometric import start_from_loading_flag
            start_game(start_from_loading_flag)

    # Créer un sous-menu pour saisir le nom
    name_menu = pygame_menu.Menu(
        'Enter Your Name', window_size[0], window_size[1], theme=pygame_menu.themes.THEME_GREEN
    )
    name_menu.add.text_input(
        'Name: ', 
        default='', 
        onchange=set_player_name, 
        textinput_id="player_name_input"
    )
    name_menu.add.button('Confirm', confirm_and_start)  # Appeler la validation
    name_menu.add.button('Cancel', pygame_menu.events.BACK)  # Revenir au menu principal
    name_menu.mainloop(surface)

def start_the_game():
    from affichage_2_5D_isometric import start_from_loading_flag
    ask_player_name()
    start_game(start_from_loading_flag)

def load_game():
    error_load_file.hide()
    main_menu._open(load_game_menu)

def settings():
    error_nb_bob_label.hide()
    main_menu._open(settings_menu)

def get_settings(): #fonction qui va save les setting quand on les valides. 
    nb_bob_selected = round(get_value_from_slider(nb_bob)[0])
    nb_food_selected = round(get_value_from_slider(nb_food)[0])
    map_length_selected = round(get_value_from_slider(map_length)[0])
    map_width_selected = round(get_value_from_slider(map_width)[0])
    indice_mutation_selected = get_value_from_slider(mutation_slider)[0]
    base_health_selected = round(get_value_from_slider(base_health_slider)[0])
    food_energy_slider_selected = round(get_value_from_slider(food_energy_slider)[0])
    if (nb_bob_selected > (map_length_selected * map_width_selected)): # Test qui lève une erreur si le nombre de bob est inférieur à la taille de la map
        error_nb_bob_label.show()
        raise ValueError("Error settings : The number of bob selecteb cannot be higher than the map size")
    print("SETTING GETTED")
    settings_menu._back()
    return (nb_bob_selected,nb_food_selected, map_length_selected,map_width_selected, settings_menu_theme.get_value(), indice_mutation_selected, base_health_selected, food_energy_slider_selected)
####################################################
def start_menu():
    global surface
    global main_menu
    global nb_bob
    global nb_food
    global map_length
    global map_width
    global load_game_menu
    global settings_menu
    global settings_menu_theme
    global mutation_slider
    global base_health_slider
    global error_nb_bob_label
    global error_load_file
    global food_energy_slider
    global player_name 

    surface = pygame.display.set_mode(window_size, RESIZABLE)
    pygame.display.set_caption('Bob: A Game of Life')
    #################### MAIN MENU ####################

    mytheme = pygame_menu.themes.THEME_GREEN.copy()
    mytheme.title_background_color=(0, 0, 0)
    myimage = pygame_menu.baseimage.BaseImage(
    image_path="sprites/background_menu_image.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    mytheme.background_color = myimage
    # main_menu = pygame_menu.Menu('Bob: A Game of Life', window_size[0], window_size[1], theme=pygame_menu.themes.THEME_GREEN)
    main_menu = pygame_menu.Menu('Bob: A Game of Life', window_size[0], window_size[1], theme=mytheme)
    main_menu.add.button('Play', start_the_game, background_color=None, font_color= ((0,0,0)), selection_color = ((255,0,0)))
    main_menu.add.button('Load Game', load_game, background_color=None, font_color= ((0,0,0)), selection_color = ((255,0,0)))
    main_menu.add.button('Settings', settings, background_color=None, font_color= ((0,0,0)), selection_color = ((255,0,0)))
    main_menu.add.button('Quit', pygame_menu.events.EXIT, background_color=None, font_color= ((0,0,0)), selection_color = ((255,0,0)))
    ################## SETTINGS MENU ##################
    settings_menu = pygame_menu.Menu('Settings', window_size[0], window_size[1], theme=pygame_menu.themes.THEME_GREEN)
    settings_menu_theme = settings_menu.add.selector("Theme: ", themes)
    # Parametre range_slider : 
    #   - 50 : Valeur par défault
    #   - (0, 100) : (min, max)
    #   - 1 : intervalle
    nb_bob = settings_menu.add.range_slider('Number of bob', 50, (1, 100), 1,
                                                rangeslider_id='nb_bob_slider',
                                                value_format=lambda x: str(int(x)))
    base_health_slider = settings_menu.add.range_slider('Base health', 100, (1, 500), 1,
                                                rangeslider_id='base_health_slider',
                                                value_format=lambda x: str(int(x)))

    nb_food = settings_menu.add.range_slider('Number of food', 50, (1, 100), 1,
                                                rangeslider_id='nb_food_slider',
                                                value_format=lambda x: str(int(x)))
    food_energy_slider = settings_menu.add.range_slider('Food energy', 100, (1, 500), 1,
                                                rangeslider_id='food_energy_slider',
                                                value_format=lambda x: str(int(x)))

    map_length = settings_menu.add.range_slider('Map height', 20, (1, 100), 1,
                                                rangeslider_id='map_length_slider',
                                                value_format=lambda x: str(int(x)))

    map_width = settings_menu.add.range_slider('Map width', 20, (1, 100), 1,
                                                rangeslider_id='map_width_slider',
                                                value_format=lambda x: str(int(x)))
    mutation_slider = settings_menu.add.range_slider('Mutation rate', 0, (0, 10), 1,
                                                rangeslider_id='Mutation_rate',
                                                value_format=lambda x: str(round(float(x), 2)))
    
    settings_confirm_button = settings_menu.add.button('Confirm', get_config_from_settings)

    error_nb_bob_label = settings_menu.add.label("Error : number of bob higher than map size", label_id="error_nb_bob_label")
    ################## LOAD GAME MENU ##################
    load_game_menu = pygame_menu.Menu('Load Game', window_size[0], window_size[1], theme=pygame_menu.themes.THEME_GREEN)
    load_game_menu_selector = load_game_menu.add.button("Load", get_config)
    error_load_file = load_game_menu.add.label("", label_id="error_load_file")
    ####################################################
    main_menu.mainloop(surface)

def get_value_from_slider(slider : pygame_menu.widgets.widget.rangeslider.RangeSlider): #prend un rangeslider en paramètre et retourne sa valeur. 
    return slider._value
    

def main_loop():
    clock = pygame.time.Clock()
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif main_menu.is_enabled():
                main_menu.update(events)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    main_menu.disable()
                    surface.fill((0, 0, 0))

        surface.fill((0, 0, 0))  # Rafraîchir l'écran
        main_menu.draw(surface)
        pygame.display.flip()
        clock.tick(60)  # Limiter la fréquence d'images à 60 FPS


