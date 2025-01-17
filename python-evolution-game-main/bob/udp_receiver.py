import socket

# Configuration du serveur (écoute sur le port 12345 et toutes les interfaces réseau)
SERVER_IP = "0.0.0.0"  # Écouter sur toutes les interfaces réseau
SERVER_PORT = 12345    # Le même port que le programme C

# Créer un socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Lier le socket à l'adresse et au port
sock.bind((SERVER_IP, SERVER_PORT))

print(f"Listening on {SERVER_IP}:{SERVER_PORT}...")

while True:
    # Réception du message
    message, addr = sock.recvfrom(1024)  # Taille maximale du message 1024 octets
    print(f"Message reçu de {addr}: {message.decode()}")

