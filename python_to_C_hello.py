'''import sys

def send_message_to_stdout():
    # Message à envoyer
    message = "hello world"
    
    # Écrire le message sur la sortie standard
    sys.stdout.write(message + "\n")
    sys.stdout.flush()  # S'assurer que le message est immédiatement envoyé

if __name__ == "__main__":
    send_message_to_stdout()'''

import socket

def send_message_udp():
    # Adresse et port du processus C
    target_ip = "127.0.0.1"  # Adresse locale (localhost)
    target_port = 12345      # Port d'écoute du processus C

    # Créer un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Message à envoyer
    message = "hello world"

    # Envoyer le message au processus C
    sock.sendto(message.encode(), (target_ip, target_port))
    print(f"Message envoyé : {message}")

if __name__ == "__main__":
    send_message_udp()

