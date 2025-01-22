import globals
from bob import Bob
import c_to_py_threading as c_py
import os

class Paquet:

    
    @staticmethod
    def export_to_ascii(file_name, dict_bob, dict_food):
        """
        Exporter les informations des dictionnaires dict_bob et dict_food dans un fichier ASCII.
        :param file_name: Nom du fichier ASCII à créer
        :param dict_bob: Dictionnaire contenant les informations des bobs
        :param dict_food: Dictionnaire contenant les informations de la nourriture
        """
        if not os.path.exists(file_name):
            open(file_name, 'w').close()
            print(f"Le fichier {file_name} n'existait pas. Il a été créé automatiquement.")


        with open(file_name, 'w', encoding='ascii') as ascii_file:
            # Export des Bobs
            ascii_file.write("BOBS\n")
            for position, bobs in dict_bob.items():
                position_str = f"{position[0]}_{position[1]}"
                for bob in bobs:
                    ascii_file.write(
                        f"{position_str},{bob.id_bob},{bob.energy},{bob.id_player},{bob.get_mass()},"
                        f"{bob.get_speed()},{bob.get_speed_buffer()},"
                        f"{bob.get_maman()},{bob.get_fils()}\n"
                    )

            # Export de la nourriture
            ascii_file.write("FOOD\n")
            for position, value in dict_food.items():
                position_str = f"{position[0]}_{position[1]}"
                ascii_file.write(f"{position_str},{value}\n")
            
            ascii_file.write("\nPLAYER\n")
            ascii_file.write(f"{globals.player_name}\n")

        print(f"Les données ont été exportées avec succès dans le fichier {file_name}.")

    @staticmethod
    def lire_distant_data(port_receive):
        """
        Au lieu d'appeler receive_message() (bloquant),
        on lit la queue c_to_py_threading.received_messages.
        Si la queue est vide => on renvoie des listes vides, rien à afficher.
        """
        bobs = []
        foods = []
        player_name = "Unknown"

        # On vérifie si on a reçu quelque chose dans la queue
        if c_py.received_messages.empty():
            # Aucune donnée => on renvoie bobs vides
            return bobs, player_name

        # Si on a des données, on prend le plus ancien message reçu
        data = c_py.received_messages.get_nowait()  # non bloquant
        if not data:
            return bobs, player_name

        # On parse la chaîne
        section = None
        lignes = data.split('\n')
        for ligne in lignes:
            ligne = ligne.strip()
            if ligne == "BOBS":
                section = "BOBS"
            elif ligne == "FOOD":
                section = "FOOD"
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
                    'fils': eval(parts[8])  # attention : évaluer la liste en clair
                })
            elif section == "FOOD" and ligne:
                parts = ligne.split(',')
                position = parts[0].split('_')
                foods.append({
                    'x': int(position[0]),
                    'y': int(position[1]),
                    'energy': int(parts[1])
                })
            elif section == "PLAYER" and ligne:
                player_name = ligne

        return bobs, player_name
