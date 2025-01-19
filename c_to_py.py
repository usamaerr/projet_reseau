import socket
import select
def receive_message(port=5005, buffer_size=1024 ,timeout=0):
    """
    Fonction pour écouter sur un port UDP avec une socket non bloquante.
    :param port: Port sur lequel écouter
    :param buffer_size: Taille maximale du message à recevoir
    :param timeout: Temps d'attente maximal en secondes
    :return: Message reçu sous forme de chaîne, ou None si aucun message reçu
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", port))
    sock.setblocking(False)

    print(f"En attente de message non bloquant sur le port {port}...")

    ready_socks, _, _ = select.select([sock], [], [], timeout)

    if ready_socks:
        message, address = sock.recvfrom(buffer_size)
        print(f"Message reçu de {address}: {message.decode()}")
        return message.decode()
    else:
        print("Aucun message reçu dans le délai imparti.")
        return None