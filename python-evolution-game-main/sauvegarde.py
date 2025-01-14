import pickle
from grid import Grid
import tkinter
import tkinter.filedialog





class Config_affichage_2_5D():
    def __init__(self, screen_height, screen_width, longueur_grille, largeur_grille, nbbob, nbfood, vitesse_actualisation, nombredefps, themeiso = "Default", indice_mutation = 0) -> None:
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.longueur_grille = longueur_grille
        self.largeur_grille = largeur_grille
        self.nbbob = nbbob
        self.nbfood = nbfood
        self.vitesse_actualisation = vitesse_actualisation
        self.nombredefps = nombredefps
        self.themeiso = themeiso
        self.indice_mutation = indice_mutation

    def return_config(self):
        return self




class Sauvegarde():
    def __init__(self, config_affichage:Config_affichage_2_5D, config_grid:Grid) -> None:
        self.config_affichage = config_affichage
        self.config_grid = config_grid




#----------------------------------------------DEFAULT CONFIGURATION----------------------------------------------------------------

screen_height = 1900  #POUR MODIFIER LA TAILLE DE LA FENETRE DE RENDU
screen_width = 1000
 
longueur_grille = 20 #POUR MODIFIER LA TAILLE DE GRILLE GENRE GRID.N ET GRID.M (POINT DE VUE LOGIQUE)
largeur_grille = 20

nbbob = 30 #POUR MODIFIER LE NOMBRE DE BOB ET DE FOOD QUI APPARAISSENT
nbfood = 199
e_spawn = 100

vitesse_actualisation = 10 #nombre d'actualisation de la grille par seconde

nombredefps = 60
#-----------------------------------------------------------------------------------------------------------------------------

config_affichage_default = Config_affichage_2_5D(screen_height, screen_width, longueur_grille, largeur_grille, nbbob, nbfood, vitesse_actualisation, nombredefps)
config_grid_default = Grid(longueur_grille,largeur_grille)
save_default = Sauvegarde(config_affichage_default, config_grid_default)



config_test = Config_affichage_2_5D(1500,1000,10,10,30,20,2,60)

grid_test = Grid(10,10)



save = Sauvegarde(config_test, grid_test)
sauvegarde_cpt = 1
def save_config():
    global sauvegarde_cpt
    with open(f'saves/sauvegarde{sauvegarde_cpt}.pkl', 'wb') as f:
        pickle.dump(save, f)
    f.close()
    sauvegarde_cpt += 1
    print("Fichier Sauvegardé !")


    
start_from_loading_flag = 0
def open_config():
    path = prompt_file()
    with open(f"{path}", 'rb') as f:
        config_loaded = pickle.load(f) # deserialize using load()
    return config_loaded #retourne l'objet de type sauvegarde
    
    
def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


