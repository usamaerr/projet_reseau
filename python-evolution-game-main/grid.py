import random
from collections import defaultdict
from datetime import datetime

import globals
from bob import Bob
from paquet import Paquet
import py_to_c_threading as py_c


class Grid:

    def __init__(self, N, M, nombre_bob_spawn = 10, nombrefood = 10, mut=0.5, bob_energy_spawn = 100, food_energy = 100):
        self.N = N #longueur 
        self.M = M #largeur
        self.dict_bob = defaultdict(None)
        self.dict_food = defaultdict(None)
        # self.create_grid()
        self.bob_energy_spawn = bob_energy_spawn
        self.tick = 0
        self.day = 0
        self.nombre_bob_spawn = nombre_bob_spawn
        self.nombrefood = nombrefood
        self.nombre_bob_actuel= 0
        self.dead_bob = [] # liste des bobs mort durant la partie
        self.indice_mut = mut 
        self.id_bob_list = [] # pour avoir des id_bob differents 
        self.food_energy = food_energy

    def init_grid(self):
        self.create_all_bob()
        self.create_all_food()
        self.nombre_bob_actuel = self.nombre_bob_spawn

    def create_grid(self):
        self.self_grid = [[0 for _ in range(self.M)] for _ in range(self.N)]


    def create_all_bob(self):
        # Création de tous les bobs initiaux dans des positions aléatoires
        
        for _ in range(self.nombre_bob_spawn):
            while True:
                x = random.randint(0, self.N-1)
                y = random.randint(0, self.M-1)
                if (x,y) not in self.dict_bob:
                    self.create_bob(x,y) 
                    self.dict_bob[(x,y)][0].set_energy(self.bob_energy_spawn)
                    break
        print("Nombre de bob créé dans le dico :", len(self.dict_bob.keys()))

    def create_bob(self, x, y ):
        # Création d'un bob à la position spécifiée
        now = datetime.now()
        min = now.min
        sec = now.second
        player_id = globals.player_name + str(min) + str(sec)
        bob = Bob(len(self.dict_bob), x, y , player_id )
        bob.id_bob = self.create_id_bob() # ajout de cette ligne pour creer des id aux bobs
        self.dict_bob[(x, y)] = [bob]

    def delete_bob(self, x, y, bob_id):
        # Suppression d'un bob à la position spécifiée avec l'ID spécifié
        if (x, y) in self.dict_bob.keys():
            for bob in self.dict_bob[(x, y)]:
                if bob.get_id() == bob_id:
                    self.dict_bob[(x, y)].remove(bob)
                    break          
    
    def delete_death_bob(self, x,y):
        # Suppression des bobs morts à la position spécifiée
        for bob in self.dict_bob[(x,y)]: 
            if bob.energy <= 0:
                self.dead_bob.append(bob)
                self.delete_bob(x,y,bob.id_bob)
                self.nombre_bob_actuel -= 1
            if len(self.dict_bob[(x,y)]) == 0:
                del(self.dict_bob[(x,y)])



    def create_all_food(self): 
        # Création de toute la nourriture initiale dans des positions aléatoires
        for _ in range(self.nombrefood):
            x = random.randint(0, self.N-1)
            y = random.randint(0, self.M-1)
            self.create_food(x,y)

    def create_food(self, x, y):
        # Création de nourriture à la position spécifiée
        if (x, y) in self.dict_food:          # Si plus d'une instance de food sont créées dans une même case, en additionner la valeur énergétique
            self.dict_food[(x, y)] += self.food_energy
        else:
            self.dict_food[(x, y)] = self.food_energy

    def new_day_food(self): 
        # Renouvellement de la nourriture chaque jour 
        self.dict_food = {}
        self.create_all_food()

    def delete_food(self, x, y):
        # Suppression de la nourriture à la position spécifiée
        if (x, y) in self.dict_food:    
            del self.dict_food[(x, y)]


                   

    def bob_eats_food(self, x,y):
        # Interaction entre les bobs et la nourriture à une position spécifiée
        for (food_x, food_y) in self.dict_food.keys():
            # Interaction entre les bobs et la nourriture à une position spécifiée
            if (x, y) == (food_x, food_y):
                bobs_at_location = self.dict_bob[(x, y)]
                if bobs_at_location:
                    bob = bobs_at_location[0]  # Accès au premier bob dans la liste

                    # Calcul de l'énergie gagnée en mangeant de la nourriture
                    energy_gained = self.dict_food[(food_x, food_y)]
                    print("bob eat : ",bob.id_bob , "food energy ", energy_gained)

                    # Vérification si l'énergie du bob plus l'énergie gagnée dépasse l'énergie maximale
                    if bob.energy + energy_gained > 200:
                        leftovers = bob.energy + energy_gained - 200
                        self.dict_food[(food_x, food_y)] = leftovers # set food energy to the leftovers
                        bob.energy = 200  # Mettre l'énergie du Bob au maximum
                    else:
                        leftovers = 0
                        bob.energy += energy_gained
                    if(leftovers == 0):
                        self.delete_food(food_x, food_y)
                        
                    return leftovers    
        return 0  # Aucun bob n'a trouvé de nourriture


#-----------------------Partie masse + mutation----------------------------------------------------------------------------------------------

    def mutation_mass(self, maman_mass):
        # Fonction pour introduire une mutation de masse basée sur la masse de la "maman"
        mut_mass = round(random.uniform(maman_mass - self.indice_mut, maman_mass + self.indice_mut), 1)
        return mut_mass


    def bob_comparison(self, bobs, ratio):                             
        # Fonction pour comparer la taille des bobs et retourner le petit et le grand
        small_bob = min(bobs, key=lambda bob: bob.get_mass())
        big_Bob = max(bobs, key=lambda bob: bob.get_mass())

        if (small_bob.get_mass()/ big_Bob.get_mass())<ratio:
            return small_bob, big_Bob
        else: 
            small_bob, big_Bob=(0,0)
            return small_bob, big_Bob

    
#---------------------------------Bob eat Bob----------------------------------------------------------------------------------------

    def eat_bob(self, small_bob, big_Bob):
        # Fonction pour permettre à un bob plus grand de manger un bob plus petit (inclut changement d'énergie et suppression du bob mangé)   
        new_energy = big_Bob.get_energy() + 0.5 * small_bob.get_energy() * (1 - small_bob.get_mass()/big_Bob.get_mass())
        big_Bob.set_energy(new_energy)
        print(f"Small bob n:{small_bob.id_bob} has been eaten by Big bob {big_Bob.id_bob}")
        print("Big Bob's new energy:", big_Bob.get_energy())  ##test
        small_bob.set_energy(0)
        self.dead_bob.append(small_bob)
        self.delete_bob(small_bob.get_x(), small_bob.get_y(), small_bob.get_id())   
        self.nombre_bob_actuel -= 1                                                                                


#------------------Partie methodes Velocité + parthenogenesis + Mut + Mass------------------------------------------------------
    def mutation_speed(self, maman_speed):
        # Fonction pour introduire une mutation de vitesse basée sur la vitesse de la "maman"
        mut_speed = round(random.uniform(maman_speed-self.indice_mut,maman_speed+self.indice_mut),1)
        return mut_speed

    def parthenogenesis(self,x,y): 
        now = datetime.now()
        min = now.min
        sec = now.second
        player_id = globals.player_name + str(min) + str(sec)
        # Fonction pour permettre la parthénogenèse (reproduction asexuée) d'un bob à la position spécifiée avec ajout de x,y pour éviter de refaire un parcours de dico a chaque fois 
        if self.dict_bob[(x, y)]:
            #verifier pour chaque bob dans la liste si l'energie = 200 et après en créer un new bob 
            for bob in self.dict_bob[(x, y)]:
                if(bob.energy >= self.bob_energy_spawn*2):
                    print("Bob partheno : ",bob.id_bob) 
                    newBob = Bob(self.create_id_bob(),x,y,player_id ,bob.get_energy()//4) # ajout de create id_bob
                    newBob.set_speed(self.mutation_speed(bob.get_speed())) # ajout de la mutation
                    newBob.set_mass(self.mutation_mass(bob.get_mass()))    #ajout de mutation de masse
                    newBob.set_maman(bob.id_bob)
                    bob.set_energy(bob.get_energy() - bob.get_energy()//4) 
                    bob.set_fils(newBob.id_bob)
                    self.dict_bob[(x, y)].append(newBob)
                    self.nombre_bob_actuel += 1 # pour tenir a jour le nb de bob sur la carte
                        
                    #reternue 
                    return (x,y)



    def create_id_bob(self):
        # Fonction pour créer un ID unique pour un nouveau bob
        id_bob = len(self.id_bob_list)+1
        self.id_bob_list.append(id_bob)
        return id_bob


    def move_random_bob_speed(self,x,y):
        # Fonction pour déplacer un bob de manière aléatoire basée sur sa vitesse
        bobs_at_location = self.dict_bob[(x, y)]
        if bobs_at_location:
            random_bob = random.choice(bobs_at_location)
    #------------------Partie Velocité----------------------------------------
            deplacement = random_bob.get_speed()+random_bob.get_speed_buffer()
            new_buffer = deplacement-int(deplacement)
            deplacement = int(deplacement)
            random_bob.set_speed_buffer(new_buffer)
    #-------------------------------------------------------------------------
            random_x, random_y = random.choice([(0, -deplacement), (0, deplacement), (-deplacement, 0), (deplacement, 0)])
            # print("deplacement : ", (random_x, random_y))
            new_x = x + random_x
            new_y = y + random_y
        if 0 <= new_x < self.N and 0 <= new_y < self.M:
            id = random_bob.id_bob

            # Conso d'énergie des bobs pour chaque déplacements en fonction de la vélocité (speed)
            random_bob.set_energy(random_bob.get_energy() - random_bob.get_mass() * max(0.5,random_bob.get_speed()**2))   ##salma - change to max speed + effet mass

            random_bob.move_bob(new_x, new_y)
            self.delete_bob(x, y, id)
            if (new_x, new_y) in self.dict_bob:
                self.dict_bob[(new_x, new_y)].append(random_bob)
                Paquet.export_to_ascii("distant_"+globals.player_name + '.txt', self.dict_bob, self.dict_food)
                py_c.send_ascii_file(filename="distant_"+globals.player_name + '.txt',target_ip="127.0.0.1",target_port=globals.port_send)
            else:
                self.dict_bob[(new_x, new_y)] = [random_bob]
                Paquet.export_to_ascii("distant_"+globals.player_name + '.txt', self.dict_bob, self.dict_food)
                py_c.send_ascii_file(filename="distant_"+globals.player_name + '.txt',target_ip="127.0.0.1",target_port=globals.port_send)
        else:
            random_bob.set_energy(random_bob.get_energy()-0.5) # ajout de cette ligne pour enlever au bob 0.5 d'energie quand ils bougent pas
            Paquet.export_to_ascii("distant_"+globals.player_name + '.txt', self.dict_bob, self.dict_food) 
            py_c.send_ascii_file(filename="distant_"+globals.player_name + '.txt',target_ip="127.0.0.1",target_port=globals.port_send)

        if len(self.dict_bob[(x,y)]) == 0:
            del(self.dict_bob[(x,y)])

            

    def action_bob_speed(self):
        # Fonction principale pour les actions des bobs basées sur la vitesse

        for (x,y) in list(self.dict_bob.keys()):
            self.delete_death_bob(x,y)
        
        for (x,y) in list(self.dict_bob.keys()):
            self.parthenogenesis(x,y)
            if (x,y) in self.dict_food.keys():
                self.bob_eats_food(x,y)
#-----------------------------------------Partie bob eatbob---------------------------------------------------------------------
            elif len(self.dict_bob[(x,y)]) > 1:
                small_bob, big_Bob = self.bob_comparison(self.dict_bob[(x,y)], ratio=2/3)
                if small_bob!= big_Bob:
                    self.eat_bob(small_bob, big_Bob)
                else:
                    self.move_random_bob_speed(x, y)
#---------------------------------------------------------------------------------------------------------------------
            else: 
                self.move_random_bob_speed(x, y)
        
        if self.tick == 100:
            self.new_day_food()
            self.day += 1
            self.tick = 0
        self.tick += 1
#------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------Reproduction sexuee ----------------------------------------------------
#    def search_eligible_pair(self, bobs, E_Reprod=150):
        # Fonction pour rechercher une paire de bobs éligibles pour la reproduction
#        for i, parent1 in enumerate(bobs[:-1]):
#            for parent2 in bobs[i+1:]:
#                if parent1.energy() >= E_Reprod and parent2.energy() >= E_Reprod:
#                    return parent1, parent2
#        return None, None
#    

#    def reproduction(self, parent1, parent2):
        # Fonction pour effectuer la reproduction entre deux parents
        #if parent1.get_energy() >= 150 and parent2.get_energy() >= 150:
#            # Calculate the average characteristics for the new Bob
#            new_energy = 100
#            new_speed = (parent1.get_speed() + parent2.get_speed()) / 2
#            new_mass = (parent1.get_mass() + parent2.get_mass()) / 2

#            self.create_bob(parent1.x, parent1.y, new_energy, new_speed, new_mass)         # Creates a new bob in the same cell

            # Decrease the energy of the parent Bobs
#            parent1.set_energy(parent1.get_energy() - 100)
#            parent2.set_energy(parent2.get_energy() - 100)

        #implementation of sexual reproduction in the action_bob function inside the elif
#                elif self.sexual_reprod_enable:             
                    # Find the first eligible pair for reproduction
#                    eligible_parent1, eligible_parent2 = self.search_eligible_pair(self.dict_bob[(x,y)])
#                    if eligible_parent1 is not None and eligible_parent2 is not None:
#                        self.reproduction(eligible_parent1, eligible_parent2)

#-----------------------------------------------------------------------------------------------------------------------------------
    
