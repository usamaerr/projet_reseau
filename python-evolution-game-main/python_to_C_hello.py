#***************** Test pour envoyer en ASCII et lire flux entrant ****************
'''
import socket
import select

def main():
    # Configurations
    send_ip = "127.0.0.1"  # IP de la machine cible pour l'envoi - localhost
    send_port = 12345         # Port pour envoyer des données au processus C
    listen_port = 12346       # Port où Python écoutera les données du processus C
    filename = "distant.txt"     # Fichier ASCII à envoyer

    # Créer le socket pour envoyer
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Créer le socket pour écouter
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.bind(("0.0.0.0", listen_port))  # Écouter sur toutes les interfaces

    print(f"Python écoute sur le port {listen_port} pour les messages du processus C...")

    # Charger les données ASCII à envoyer
    try:
        with open(filename, 'r') as file:
            ascii_data = file.read()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {filename} : {e}")
        return

    # Boucle principale
    while True:
        # Utiliser select() pour surveiller les sockets
        read_sockets, _, _ = select.select([listen_socket], [], [], 1)

        # Si le socket d'écoute est prêt, lire les données reçues
        for sock in read_sockets:
            if sock == listen_socket:
                data, addr = listen_socket.recvfrom(65536)
                print(f"Message reçu de {addr} :\n{data.decode('utf-8')}")

        # Envoyer les données ASCII si nécessaire
        # Par exemple, on peut envoyer à intervalles réguliers ou sur un événement
        send_socket.sendto(ascii_data.encode('utf-8'), (send_ip, send_port))
        print(f"Fichier {filename} envoyé à {send_ip}:{send_port} :\n{ascii_data}")
        break  # Supprimez le break pour maintenir l'envoi continu si nécessaire

if __name__ == "__main__":
    main()




'''








#****************   Test sur sortie standard  **********
'''
import sys

def send_message_to_stdout():
    # Message à envoyer
    message = "hello world"
    
    # Écrire le message sur la sortie standard
    sys.stdout.write(message + "\n")
    sys.stdout.flush()  # S'assurer que le message est immédiatement envoyé

if __name__ == "__main__":
    send_message_to_stdout()'''




#****************  Test hello world avec UDP  **********************
'''import socket

def send_message_udp():
    # Adresse et port du processus C
    target_ip = "127.0.0.1"  # localhost
    target_port = 12345      # Port d'écoute du processus C

    # Créer un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Message à envoyer
    message = "hello world"

    # Envoyer le message au processus C
    sock.sendto(message.encode(), (target_ip, target_port))
    print(f"Message envoyé : {message}")

if __name__ == "__main__":
    send_message_udp()'''






#**************************  Test pour envoyer données en ASCII ****************


import socket

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

if __name__ == "__main__":
    # Exemple d'utilisation
    send_ascii_file(
        filename="distant.txt",       # Nom du fichier ASCII
        target_ip="127.0.0.1",  # Adresse IP localhost
        target_port=5001          # Port de destination
    )












