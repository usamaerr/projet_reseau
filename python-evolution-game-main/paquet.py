import json


class Paquet:
    
    def export_to_json(file_name, dict_bob, dict_food):
        """
        Exporter les informations des dictionnaires dict_bob et dict_food vers un fichier JSON.
        :param file_name: Nom du fichier JSON à créer
        :param dict_bob: Dictionnaire contenant les informations des bobs
        :param dict_food: Dictionnaire contenant les informations de la nourriture
        """
        # Transformer dict_bob en une structure sérialisable
        bobs_data = {
            f"{position[0]}_{position[1]}": [
                {
                    "id": bob.id_bob,
                    "energy": bob.energy,
                    "mass": bob.get_mass(),
                    "speed": bob.get_speed(),
                    "attributes": {
                        "speed_buffer": bob.get_speed_buffer(),
                        "maman": bob.get_maman(),
                        "fils": bob.get_fils()
                    }
                }
                for bob in bobs
            ]
            for position, bobs in dict_bob.items()
        }

        # Transformer dict_food en une structure sérialisable
        food_data = {
            f"{position[0]}_{position[1]}": value
            for position, value in dict_food.items()
        }

        # Préparer les données combinées
        data = {
            "bobs": bobs_data,
            "food": food_data
        }

        # Sauvegarder dans un fichier JSON
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"Les données ont été exportées avec succès dans le fichier {file_name}")
