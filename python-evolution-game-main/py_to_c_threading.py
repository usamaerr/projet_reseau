import socket
import threading

# Sémaphore pour synchroniser l'envoi et la réception
send_semaphore = threading.Semaphore(1)  # Un seul thread peut envoyer à la fois

def send_ascii_file(filename, target_ip, target_port):
    """
    Envoie un fichier ASCII à une adresse IP et un port spécifiés.
    :param filename: Nom du fichier ASCII à envoyer
    :param target_ip: Adresse IP de destination
    :param target_port: Port de destination
        """
    # Acquérir le sémaphore pour garantir l'exclusion mutuelle
    with send_semaphore:
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

# Exemple d'utilisation avec threading
def send_file_thread(filename, target_ip, target_port):
    """
    Fonction pour exécuter l'envoi de fichier dans un thread.
    """
    thread = threading.Thread(target=send_ascii_file, args=(filename, target_ip, target_port))
    thread.start()
    return thread

# Exemple d'utilisation
# if __name__ == "__main__":
#     filename = "example.txt"
#     target_ip = "127.0.0.1"
#     target_port = 5000

#     # Lancer l'envoi dans un thread
#     send_thread = send_file_thread(filename, target_ip, target_port)
#     send_thread.join()  # Attendre que le thread se termine
