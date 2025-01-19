import socket
import globals

def send_ascii_file(filename, target_ip, target_port):
    # Lire le contenu du fichier ASCII
    try:
        with open(filename, 'r') as file:
            ascii_data = file.read()  # Lire tout le fichier en une seule chaîne
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier ASCII : {e}")
        return

    # Convertir la chaîne en octets pour l'envoi
    ascii_bytes = ascii_data.encode('utf-8')

    # Créer un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Envoyer le contenu ASCII
    sock.sendto(ascii_bytes, (target_ip, target_port))
    print(f"Fichier ASCII envoyé à {target_ip}:{target_port} :\n{ascii_data}")

