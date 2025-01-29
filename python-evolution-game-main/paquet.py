import globals
from bob import Bob
import c_to_py_threading as c_py
import os
import ast 
bobs_distant_cache = []
player_name_cache = "Unknown"


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

    def lire_distant_data(port_receive):
        """
        Au lieu d'appeler receive_message() (bloquant),
        on lit la queue c_to_py_threading.received_messages.
        Si la queue est vide => on renvoie les derniers bobs connus.
        """
        global bobs_distant_cache, player_name_cache
        bobs = []
        player_name = player_name_cache

        # Vérifier si on a reçu un message dans la queue
        if not c_py.received_messages.empty():
            # Récupérer les nouvelles données
            data = c_py.received_messages.get_nowait()  # non bloquant
            if data:
                bobs, player_name = Paquet.traiter_donnees_reçues(data)

                # Si des bobs ont été reçus, on met à jour le cache
                if bobs:
                    bobs_distant_cache = bobs
                if player_name != "Unknown":  # On garde le dernier nom valide
                    player_name_cache = player_name
            else:
                return bobs_distant_cache, player_name  # Aucune donnée reçue, on renvoie le cache
        else:
            return bobs_distant_cache, player_name  # Queue vide, on renvoie les derniers bobs connus

        return bobs, player_name

    def traiter_donnees_reçues(data):
        """ Fonction qui parse les données reçues. """
        bobs = []
        player_name = "Unknown"
        section = None
        lignes = data.split('\n')

        for ligne in lignes:
            ligne = ligne.strip()
            if ligne == "BOBS":
                section = "BOBS"
            elif ligne == "PLAYER":
                section = "PLAYER"
            elif section == "BOBS" and ligne:
                parts = ligne.split(',')
                try:
                    position = parts[0].split('_')
                    x = int(position[0])
                    y = int(position[1])
                    id_bob = parts[1]
                    energy = float(parts[2])
                    id_player = parts[3]
                    mass = float(parts[4])
                    speed = float(parts[5])
                    speed_buffer = float(parts[6])
                    maman = int(parts[7])
                    try:
                        # Vérifier que la chaîne est bien une liste et qu'elle est correctement fermée
                        if parts[8].startswith("[") and parts[8].endswith("]"):
                            fils = ast.literal_eval(parts[8])  # Convertir en liste Python
                            if not isinstance(fils, list):  # Vérifier que c'est bien une liste
                                fils = []
                        else:
                            fils = []  # Si ce n'est pas une liste correctement fermée, on ignore
                    except (SyntaxError, ValueError):
                        fils = []  # Si la liste est mal formée, on la vide


                    bobs.append({
                        'x': x, 'y': y, 'id_bob': id_bob, 'energy': energy,
                        'id_player': id_player, 'mass': mass, 'speed': speed,
                        'speed_buffer': speed_buffer, 'maman': maman, 'fils': fils
                    })
                except (ValueError, IndexError):
                    print(f"Erreur parsing BOBS : {ligne}")

            elif section == "PLAYER" and ligne:
                player_name = ligne
                print(f"[DEBUG] Nom du joueur distant reçu : {player_name}")  # Debug pour voir les noms reçus


        return bobs, player_name


    
