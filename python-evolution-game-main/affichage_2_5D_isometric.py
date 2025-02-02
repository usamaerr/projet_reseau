from random import *
from time import *

import pygame
from pygame.locals import *

import globals
from grid import Grid
from paquet import Paquet
from sauvegarde import (open_config, save_config, save_default,
                        start_from_loading_flag)

configuration = save_default
def get_config():
    global configuration
    global start_from_loading_flag 
    try:
        configuration = open_config()
    except FileNotFoundError:
        from menu import error_load_file
        error_load_file.set_title("Error : No file selected")
        error_load_file.show()
        print("Error load save : No file selected")
    except Exception:
        from menu import error_load_file
        error_load_file.set_title("Error : Wrong file type selected, <file>.pkl required")
        error_load_file.show()
        print("Error load save : Wrong file type selected (<file>.pkl required)")
    else:
        from menu import load_game_menu
        start_from_loading_flag = 1
        print("Configuration chargée !")
        load_game_menu._back()
        return configuration

def get_config_from_settings():
    global configuration
    from menu import get_settings
    try:
        settings = get_settings()
    except ValueError as ve:
        print(ve)
    else:
        configuration.config_affichage.nbbob = settings[0]
        configuration.config_grid.nombre_bob_spawn = settings[0]
        configuration.config_affichage.nbfood = settings[1]
        configuration.config_grid.nombrefood = settings[1]
        configuration.config_affichage.longueur_grille = settings[2]
        configuration.config_grid.N = settings[2]
        configuration.config_affichage.largeur_grille = settings[3]
        configuration.config_grid.M = settings[3]
        configuration.config_affichage.themeiso = settings[4][0][0]
        configuration.config_affichage.indice_mutation = settings[5]
        configuration.config_grid.indice_mut = settings[5]
        configuration.config_grid.bob_energy_spawn = settings[6]
        configuration.config_grid.food_energy = settings[7]
        set_theme(configuration.config_affichage.themeiso)
        print(configuration.config_affichage.nbbob)
        print("Configuration chargée !")
        return configuration
    
print(configuration.config_affichage.longueur_grille, configuration.config_affichage.largeur_grille)
# displaysurf = pygame.display.set_mode((configuration.config_affichage.screen_height, configuration.config_affichage.screen_width), FULLSCREEN | SCALED)    #set the display mode, window title and FPS clock
# pygame.display.set_caption('BLOB ADVENTURE ')
# FPSCLOCK = pygame.time.Clock()




# grid_width = configuration.config_affichage.longueur_grille*64
# grid_height = configuration.config_affichage.largeur_grille*64

# grid_surface = pygame.Surface((grid_height + 64,grid_width + 64 )) 
# item_surface = pygame.Surface((grid_height + 64,grid_width + 64))
# screen_surface = pygame.Surface((configuration.config_affichage.screen_height, configuration.config_affichage.screen_width))  # Taille de l'écran

# grid_offset_x = (configuration.config_affichage.screen_height - grid_height) // 2

# grid_offset_y = ( configuration.config_affichage.screen_width -  grid_width ) // 2


def redefinition_surface():
    global displaysurf
    global grid_surface
    global item_surface
    global screen_surface
    global grid_offset_x
    global grid_offset_y
    global FPSCLOCK

    displaysurf = pygame.display.set_mode((configuration.config_affichage.screen_height, configuration.config_affichage.screen_width), RESIZABLE)    #set the display mode, window title and FPS clock
    pygame.display.set_caption('Bob : a Game of Life ')
    FPSCLOCK = pygame.time.Clock()
    grid_width = configuration.config_affichage.longueur_grille*64
    grid_height = configuration.config_affichage.largeur_grille*64

    grid_surface = pygame.Surface((grid_height + 64,grid_width + 64 )) 
    item_surface = pygame.Surface((grid_height + 64,grid_width + 64))
    screen_surface = pygame.Surface((configuration.config_affichage.screen_height, configuration.config_affichage.screen_width))  # Taille de l'écran

    grid_offset_x = (configuration.config_affichage.screen_height - grid_height) // 2

    grid_offset_y = ( configuration.config_affichage.screen_width -  grid_width ) // 2

theme = "Default"
def set_theme(value = "Default"):
    global theme
    global bobsprite
    global grass
    global food
    global bobpath
    global grasspath
    global foodpath
    global overlay_image
    global overlay_image_red
    print(value)
   
    theme = value
    bobsprite = pygame.image.load(f'sprites/base_{theme}_patrick.png').convert_alpha()
    grass = pygame.image.load(f'sprites/{theme}_grass.png').convert_alpha()
    food = pygame.image.load(f'sprites/{theme}_food.png').convert_alpha()
    bobpath = f"{theme}_patrick.png"
    grasspath = f"{theme}_grass.png"
    foodpath = f"{theme}_food.png"
    bobsprite.set_colorkey((0,0,0))
    grass.set_colorkey((0,0,0))
    food.set_colorkey((0,0,0))


    overlay_image = pygame.image.load("sprites/overlay_test.png").convert_alpha()
    overlay_image_red = pygame.image.load("sprites/overlay_test_red.png").convert_alpha()
    overlay_image.set_colorkey((0,0,0))
    overlay_image_red.set_colorkey((0,0,0))
        
#---------------------------------------IMPORT IMAGES DIMENSION--------------------------------------
  #load images


#test = pygame.image.load('sprites/test.png')

#test.set_colorkey((0,0,0))
#-------------------------------------------------------------------------------------------------

TILEWIDTH = 64  #holds the tile width and height
TILEHEIGHT = 64
TILEHEIGHT_HALF = TILEHEIGHT /2
TILEWIDTH_HALF = TILEWIDTH /2


def draw_initial_grid_v2(mygrid:Grid ): #tentative de modification/optimisation des fonctions de créations pour ne plus passer par les fonction create_map()
    for n in range(0,mygrid.N):   #for every row of the map...
        for m in range(0, mygrid.M):
                tileImage = grass
                cart_x = n * TILEWIDTH_HALF
                cart_y = m * TILEHEIGHT_HALF  
                iso_x = (cart_x - cart_y) 
                iso_y = (cart_x + cart_y)/2 
                centered_x = grid_surface.get_rect().centerx + iso_x
                centered_y = grid_surface.get_rect().centery/2 + iso_y
                grid_surface.blit(tileImage, (centered_x, centered_y)) #display the actual tile

          
def draw_full_grid_v2(mygrid: Grid , port_receiver ):
    global bobsprite
    global grass
    global food

    # Fonction pour lire les données du fichier distant.txt
    bobs_distant,  player_name = Paquet.lire_distant_data(port_receiver)
    

    # Dessiner la grille
    for n in range(0, mygrid.N):   # Pour chaque ligne de la carte...
        for m in range(0, mygrid.M):
            cart_x = n * TILEWIDTH_HALF
            cart_y = m * TILEHEIGHT_HALF
            iso_x = (cart_x - cart_y)
            iso_y = (cart_x + cart_y) / 2
            centered_x = grid_surface.get_rect().centerx + iso_x
            centered_y = grid_surface.get_rect().centery / 2 + iso_y
            font = pygame.font.Font(None, 24)

            if mygrid.dict_bob.get((n, m)) is None and mygrid.dict_food.get((n, m)) is None:
                # Case vide, afficher l'herbe
                tileImage = grass
                centered_x1 = grid_surface.get_rect().centerx + iso_x
                centered_y1 = grid_surface.get_rect().centery / 2 + iso_y
                grid_surface.blit(tileImage, (centered_x1, centered_y1))

            elif mygrid.dict_bob.get((n, m)) is not None:
                # Dessiner les bobs locaux
                for bob in mygrid.dict_bob[(n, m)]:
                    if bob.energy <= 0.25 * mygrid.bob_energy_spawn:
                        bobsprite = changecolor(bobsprite, "red")
                    elif bob.energy <= 0.50 * mygrid.bob_energy_spawn:
                        bobsprite = changecolor(bobsprite, "yellow")
                    else:
                        bobsprite = changecolor(bobsprite, "base")
                    tileImage = bobsprite
                    item_surface.blit(tileImage, (centered_x, centered_y))

                    # Dessiner le nom "Local" au-dessus
                    text_surface = font.render(globals.player_name, True, (255, 255, 255))  # Texte blanc
                    text_rect = text_surface.get_rect(center=(centered_x + bobsprite.get_width() // 2, centered_y - 10))
                    item_surface.blit(text_surface, text_rect)

            elif mygrid.dict_food.get((n, m)) is not None:
                # Dessiner la nourriture
                tileImage = food
                item_surface.blit(tileImage, (centered_x, centered_y))
    
    # Dessiner les bobs distants
    for bob in bobs_distant:
        n, m = bob['x'], bob['y']
        cart_x = n * TILEWIDTH_HALF
        cart_y = m * TILEHEIGHT_HALF
        iso_x = (cart_x - cart_y)
        iso_y = (cart_x + cart_y) / 2
        centered_x = grid_surface.get_rect().centerx + iso_x
        centered_y = grid_surface.get_rect().centery / 2 + iso_y

        bobsprite = changecolor(bobsprite, "yellow")
        tileImage = bobsprite
        item_surface.blit(tileImage, (centered_x, centered_y))

        # Dessiner le nom du joueur au-dessus
        font = pygame.font.Font(None, 24)
        text_surface = font.render(player_name, True, (255, 255, 255))  # Texte blanc
        text_rect = text_surface.get_rect(center=(centered_x + bobsprite.get_width() // 2, centered_y - 10))
        item_surface.blit(text_surface, text_rect)
            
            

def draw_visible_grid(grid_offset_x, grid_offset_y): 
    # Dessiner la portion visible de la grille sur screen_surface en utilisant les coordonnées décalées
    # visible_rect = pygame.Rect(grid_offset_x, grid_offset_y, screen_height, screen_width)
    screen_surface.fill((0,0,0))
    grid_surface.set_colorkey((0,0,0))
    item_surface.set_colorkey((0,0,0))
    screen_surface.blit(grid_surface, (grid_offset_x, grid_offset_y))
    screen_surface.blit(item_surface, (grid_offset_x, grid_offset_y))
    item_surface.fill((0,0,0))


#---------------------------------FONCTIONS OVERLAY--------------------------------------------------
def Render_Text(what, color, where, font=("Arial", 24)):
    """
    what : string à afficher
    color : couleur rgb (tuple) ex=>(255,0,0) rouge
    where : position sur l'écran (tuple) origine=>Nord-Ouest
    font : police d'écriture (tuple) par defaut=> ("Arial", 24)
    """
    police = pygame.font.SysFont(font[0], font[1])
    text = police.render(what, 1, pygame.Color(color))
    displaysurf.blit(text, where)

orgine_overlay_test = (80,60)
def Render_Text_OverlayTest(what, color,next_down=1, font=("Arial", 24)):
    """ 
    La même que Render_Text() mais avec un placement du texte automatiser en fonction de font.
    next_down : placement du texte en fonction de l'origine => 1 : origine ; 2 : à coter ; -1 en dessous  ; -2 en dessous origine etc...
    """

    police = pygame.font.SysFont(font[0], font[1])
    text = police.render(what, 1, pygame.Color(color))
    if next_down > 0:
        if next_down == 1:
            where = orgine_overlay_test
        else:
            where = (orgine_overlay_test[0]+next_down*(font[1]+5+len(what)),orgine_overlay_test[1])
    else:
        if next_down == -1:
            where = (80,105)
        else:
            where = (orgine_overlay_test[0]+abs(next_down)*(font[1]+5+len(what)),orgine_overlay_test[1]+(font[1]+20))
    
    displaysurf.blit(text, where)


def Render_Text_OverlayTest_red(what, color,next_down=1, font=("Arial", 24)):
    orgine_overlay_test_red = (displaysurf.get_width()-580,60)
    police = pygame.font.SysFont(font[0], font[1])
    text = police.render(what, 1, pygame.Color(color))
    if next_down > 0:
        if next_down == 1:
            where = orgine_overlay_test_red
        else:
            where = (orgine_overlay_test_red[0]+next_down*(font[1]+30),orgine_overlay_test_red[1])
    else:
        if next_down == -1:
            where = (80,105)
        else:
            where = (orgine_overlay_test_red[0]+abs(next_down)*(font[1]+20),orgine_overlay_test_red[1]+(font[1]*2))
    
    displaysurf.blit(text, where)
citation_enterrement_bob = [ "Ici repose un(e) ami(e) bien-aimé(e).", "À jamais dans nos cœurs.","Sa lumière continue de briller parmi nous.","Parti(e) trop tôt, mais jamais oublié(e).","L'amour ne meurt jamais.","Le souvenir est le trésor du cœur.","Il/elle a laissé une empreinte indélébile sur nos vies.","Un(e) être cher(e) qui vivra éternellement dans nos souvenirs.","À la mémoire d'une vie bien vécue.","Le silence est d'or, mais les souvenirs sont inestimables.","Dans la paix éternelle, qu'il/elle repose en toute sérénité.","À celui/celle qui a aimé et a été aimé(e).","Une étoile brillante s'est éteinte dans notre ciel.","La vie est éphémère, mais l'amour est éternel.","Le voyage de la vie est achevé, mais l'esprit perdure.","Son esprit vivra toujours dans nos pensées."]
prenom_bob = [ "Achille","Héraclès","Persephone","Oedipe","Electre", "Agamemnon","Penelope","Thésée", "Antigone","Icare","Andromaque","Hélène","Orphée","Cassandre","Hermione","Prométhée","Chryséis","Jason","Aphrodite","Ajax","Elizabeth","Dorian", "Heathcliff","Emma","Atticus","Elinor","Pip","Jane","Fitzwilliam","Darcy","Gatsby", "Victor","Catherine","Romeo","Juliet", "Oliver"]
def affichage_bob_morts(gridou):
    if gridou.dead_bob:
        index = gridou.dead_bob[-1].id_bob
        while index >= len(prenom_bob):
            index -= len(prenom_bob)
        texte_mort1 = prenom_bob[index] + ", le bob numéro " + str(gridou.dead_bob[-1].id_bob)
        index = gridou.dead_bob[-1].id_bob
        while index >= len(citation_enterrement_bob):
            index -= len(citation_enterrement_bob)
        texte_mort2 = " - " + citation_enterrement_bob[index]
        return texte_mort1, texte_mort2
    else:
        return "Aucun bob n'est mort !", ""


#----------------------------------------------------------------------------------------------------


nouvelle_couleur = (255, 0, 0)

def changecolor(sprite, color):
    sprite = pygame.image.load(f"sprites/{color}_{bobpath}").convert_alpha()
    return sprite

class Bouton:
    def __init__(self, x, y, largeur, hauteur, couleur_normale, couleur_survole, texte, fonction):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.couleur_normale = couleur_normale
        self.couleur_survole = couleur_survole
        self.texte = texte
        self.fonction = fonction
        self.survol = False

    def dessiner(self):
        # Changer la couleur du bouton en fonction du survol
        couleur = self.couleur_survole if self.survol else self.couleur_normale
        pygame.draw.rect(displaysurf, couleur, self.rect)
        font=("Arial", 24)
        police = pygame.font.SysFont(font[0], font[1])
        NOIR = (255,255,255)
        # Afficher le texte du bouton
        texte_surface = police.render(self.texte, True, NOIR)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        displaysurf.blit(texte_surface, texte_rect)
        

bouton = Bouton(orgine_overlay_test[0], orgine_overlay_test[1] + 100, 200, 50, (0, 255, 0), (0, 200, 0), "Sauvegarder", save_config)