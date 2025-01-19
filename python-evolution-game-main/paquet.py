import globals
from bob import Bob
import c_to_py as c_py
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
        Fonction pour lire les données reçues par UDP et les convertir en listes de bobs et de nourritures.
        :return: (liste de bobs, nom du joueur)
        """
        bobs = []
        foods = []
        player_name = "Unknown"
        section = None
        try:
            # Recevoir le message via UDP
            
            data = c_py.receive_message(port=port_receive)
            lignes = data.split('\n')  # Diviser les données en lignes

            for ligne in lignes:
                ligne = ligne.strip()
                # Identifier les sections du message
                if ligne == "BOBS":
                    section = "BOBS"
                elif ligne == "FOOD":
                    section = "FOOD"
                elif ligne == "PLAYER":
                    section = "PLAYER"
                elif section == "BOBS" and ligne:
                    # Extraire les données des bobs
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
                        'fils': eval(parts[8])  # Convertir la liste des fils
                    })
                elif section == "FOOD" and ligne:
                    # Extraire les données de la nourriture
                    parts = ligne.split(',')
                    position = parts[0].split('_')
                    foods.append({
                        'x': int(position[0]),
                        'y': int(position[1]),
                        'energy': int(parts[1])
                    })
                elif section == "PLAYER" and ligne:
                    # Extraire le nom du joueur
                    player_name = ligne
        except Exception as e:
            print(f"Erreur lors de la réception des données : {e}")

        return bobs, player_name

