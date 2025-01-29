import globals
from bob import Bob
import c_to_py_threading as c_py
import os
import ast
import json  

class Paquet:

    @staticmethod
    def export_to_ascii(file_name, moved_bob):
        """
        Exporter les informations d'un seul Bob déplacé dans un fichier ASCII et concaténer les nouvelles données.
        :param file_name: Nom du fichier ASCII à créer
        :param moved_bob: Bob qui s'est déplacé et dont les informations doivent être mises à jour
        """
        if not os.path.exists(file_name):
            open(file_name, 'w').close()
            print(f"Le fichier {file_name} n'existait pas. Il a été créé automatiquement.")
            with open(file_name, 'a', encoding='ascii') as ascii_file:
                ascii_file.write("PLAYER\n")
                ascii_file.write(f"{globals.player_name}\n")
                ascii_file.write("BOBS\n")    

        with open(file_name, 'a', encoding='ascii') as ascii_file:  # Ouverture en mode ajout
            # Export du Bob déplacé
            position_str = f"{moved_bob.get_x()}_{moved_bob.get_y()}"
            ascii_file.write(
                f"{position_str},{moved_bob.id_bob},{moved_bob.energy},{moved_bob.id_player},{moved_bob.get_mass()},"
                f"{moved_bob.get_speed()},{moved_bob.get_speed_buffer()},"
                f"{moved_bob.get_maman()},{moved_bob.get_fils()}\n"
            )
        print(f"Les données mises à jour ont été ajoutées dans le fichier {file_name}.")

    def supprimer_fichier(file_name):
        """
        Supprime le fichier après le déplacement de tous les Bobs.
        :param file_name: Nom du fichier ASCII à supprimer
        """
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Le fichier {file_name} a été supprimé après le déplacement de tous les Bobs.")
        else:
            print(f"Le fichier {file_name} n'existe pas.")

    @staticmethod
    def lire_distant_data(port_receive,json_file=None):
        """
        Au lieu d'appeler receive_message() (bloquant),
        on lit la queue c_to_py_threading.received_messages.
        Si la queue est vide => on renvoie des listes vides, rien à afficher.
        """
        if json_file is None:
            json_file = f"receive_data_{globals.player_name}.json"
        
        bobs = []
        foods = []
        player_name = "Unknown"


        # Vérifier si on a reçu des données
        if c_py.received_messages.empty():
            # Charger les données depuis le fichier JSON si présent
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("bobs", []), data.get("player_name", "Unknown")
            return bobs, player_name
        
        # Si on a des données, on prend le plus ancien message reçu
        data = c_py.received_messages.get_nowait()  # non bloquant
        # # if not data:
        # #     return bobs, player_name

        # On parse la chaîne
        section = None
        lignes = data.split('\n')
        for ligne in lignes:
            ligne = ligne.strip()
            if ligne == "BOBS":
                section = "BOBS"
            # elif ligne == "FOOD":
            #     section = "FOOD"
            elif ligne == "PLAYER":
                section = "PLAYER"
            elif section == "BOBS" and ligne:
                parts = ligne.split(',')
                position = parts[0].split('_')
                bobs.append({
                    'x': int(position[0]),
                    'y': int(position[1]),
                    'id_bob': parts[1],
                    'energy': float(parts[2]),
                    'id_player': parts[3],
                    'mass': float(parts[4]),
                    'speed': float(parts[5]),
                    'speed_buffer': float(parts[6]),
                    'maman': int(parts[7]),
                    'fils': ast.literal_eval(parts[8]) if parts[8].startswith("[") and parts[8].endswith("]") else []
                })
            # elif section == "FOOD" and ligne:
            #     parts = ligne.split(',')
            #     position = parts[0].split('_')
            #     foods.append({
            #         'x': int(position[0]),
            #         'y': int(position[1]),
            #         'energy': int(parts[1])
            #     })
            elif section == "PLAYER" and ligne:
                player_name = ligne
        if not os.path.exists(json_file):
            open(json_file, 'w').close()
            print(f"Le fichier {json_file} n'existait pas. Il a été créé automatiquement.")
        # Sauvegarder les données reçues dans un fichier JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({"bobs": bobs, "player_name": player_name}, f, indent=4)
        return bobs, player_name
