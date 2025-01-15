from bob import Bob


class Paquet:

    @staticmethod
    def export_to_ascii(file_name, dict_bob, dict_food):
        """
        Exporter les informations des dictionnaires dict_bob et dict_food dans un fichier ASCII.
        :param file_name: Nom du fichier ASCII à créer
        :param dict_bob: Dictionnaire contenant les informations des bobs
        :param dict_food: Dictionnaire contenant les informations de la nourriture
        """
        with open(file_name, 'w', encoding='ascii') as ascii_file:
            # Export des Bobs
            ascii_file.write("BOBS\n")
            for position, bobs in dict_bob.items():
                position_str = f"{position[0]}_{position[1]}"
                for bob in bobs:
                    ascii_file.write(
                        f"{position_str},{bob.id_bob},{bob.energy},{bob.get_mass()},"
                        f"{bob.get_speed()},{bob.get_speed_buffer()},"
                        f"{bob.get_maman()},{bob.get_fils()}\n"
                    )

            # Export de la nourriture
            ascii_file.write("FOOD\n")
            for position, value in dict_food.items():
                position_str = f"{position[0]}_{position[1]}"
                ascii_file.write(f"{position_str},{value}\n")

        print(f"Les données ont été exportées avec succès dans le fichier {file_name}.")

    @staticmethod
    def import_from_ascii(file_name):
        """
        Importer les informations des dictionnaires dict_bob et dict_food depuis un fichier ASCII.
        :param file_name: Nom du fichier ASCII à lire
        :return: dict_bob et dict_food reconstruits
        """
        dict_bob = {}
        dict_food = {}
        with open(file_name, 'r', encoding='ascii') as ascii_file:
            mode = None
            for line in ascii_file:
                line = line.strip()
                if line == "BOBS":
                    mode = "BOBS"
                    continue
                elif line == "FOOD":
                    mode = "FOOD"
                    continue

                if mode == "BOBS":
                    position_str, id_bob, energy, mass, speed, speed_buffer, maman, fils = line.split(',')
                    position = tuple(map(int, position_str.split('_')))
                    bob = Bob(
                        id_bob=int(id_bob),
                        energy=float(energy),
                        mass=float(mass),
                        speed=float(speed),
                        speed_buffer=float(speed_buffer),
                        maman=maman,
                        fils=fils
                    )
                    if position not in dict_bob:
                        dict_bob[position] = []
                    dict_bob[position].append(bob)
                elif mode == "FOOD":
                    position_str, value = line.split(',')
                    position = tuple(map(int, position_str.split('_')))
                    dict_food[position] = int(value)

        print(f"Les données ont été importées avec succès depuis le fichier {file_name}.")
        return dict_bob, dict_food
