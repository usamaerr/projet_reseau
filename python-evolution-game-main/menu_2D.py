import configparser
import subprocess

import pygame
import pygame_menu

window_size = ((900, 700))

pygame.init()
surface = pygame.display.set_mode(window_size)

# Function to read settings from the configuration file
def read_settings_file():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Read the 'nb_bob' value
    nb_bob = int(config['Dimensions']['nb_bob'])
    nb_food = int(config['Dimensions']['nb_food'])
    width = int(config['Dimensions']['width'])
    height = int(config['Dimensions']['height'])
    energie = int(config['Dimensions']['energie'])
    mut_rate = config['Dimensions']['mut_rate']

    return {'nb_bob': nb_bob,'nb_food': nb_food,'width': width,'height': height , 'energie': energie , 'mut_rate': mut_rate }

def update_settings_file(settings):
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Update or add the 'nb_bob' value
    config['Dimensions']['nb_bob'] = str(settings['nb_bob'])
    config['Dimensions']['nb_food'] = str(settings['nb_food'])
    config['Dimensions']['width'] = str(settings['width'])
    config['Dimensions']['height'] = str(settings['height'])
    config['Dimensions']['energie'] = str(settings['energie'])
    config['Dimensions']['mut_rate'] = str(settings['mut_rate'])

    # Write the updated configuration to the file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Initial values for settings
settings_values = read_settings_file()
def settings_menu():
    global settings_values

    def update_nb_bob(value, **kwargs):
        settings_values['nb_bob'] = int(value)
        update_settings_file(settings_values)

    def update_nb_food(value, **kwargs):
        settings_values['nb_food'] = value  
        update_settings_file(settings_values)
    
    def update_width(value, **kwargs):
        settings_values['width'] = int(value)
        update_settings_file(settings_values)

    def update_height(value, **kwargs):
        settings_values['height'] = int(value)
        update_settings_file(settings_values)

    def update_energie(value, **kwargs):
        settings_values['energie'] = int(value)
        update_settings_file(settings_values)

    def update_mut_rate(value, **kwargs):
        settings_values['mut_rate'] = value
        update_settings_file(settings_values)


    settings_menu = pygame_menu.Menu('Settings', window_size[0], window_size[1], theme=pygame_menu.themes.THEME_GREEN)

    # Add a text input field for nb_bob
    settings_menu.add.text_input('Number of Bobs: ', default=str(settings_values['nb_bob']), onchange=update_nb_bob)
    settings_menu.add.text_input('Number of Foods: ', default=str(settings_values['nb_food']), onchange=update_nb_food)
    settings_menu.add.text_input('Width: ', default=str(settings_values['width']), onchange=update_width)
    settings_menu.add.text_input('Height: ', default=str(settings_values['height']), onchange=update_height)
    settings_menu.add.text_input('Energie: ', default=str(settings_values['energie']), onchange=update_energie)
    settings_menu.add.text_input('mut_rate: ', default=str(settings_values['mut_rate']), onchange=update_mut_rate)

    # Add a button to apply the settings and return to the main menu
    settings_menu.add.button('Apply', lambda: settings_menu.disable())

    # Add a button to return to the main menu without applying changes
    settings_menu.add.button('Back', lambda: settings_menu.disable())

    settings_menu.mainloop(surface)

def settings():

    pass

def start_menu_2D():
    subprocess.run(["python", "menu_2D.py"])

def start_the_game():
    subprocess.run(["python", "affichage_2D.py"])


menu = pygame_menu.Menu('Bob : A game of life', window_size[0], window_size[1],
                       theme=pygame_menu.themes.THEME_GREEN)


menu.add.button('Play', start_the_game)
menu.add.button('Settings', settings_menu)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
