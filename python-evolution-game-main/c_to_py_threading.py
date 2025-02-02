# c_to_py_threading.py

import socket
import select
import threading
import queue

# Queue où l'on stocke les messages reçus
received_messages = queue.Queue()

def network_listener(port=5005, buffer_size=1024, timeout=5):
    """
    Thread listener pour recevoir les messages sur un port UDP donné.
    La fonction tourne en boucle et place les données reçues dans received_messages.
    """
    # Créer le socket en mode UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", port))
    sock.setblocking(False)

    print(f"[network_listener] Écoute non bloquante sur le port {port}...")

    while True:
        # On utilise select.select avec un timeout pour éviter de bloquer indéfiniment
        ready_socks, _, _ = select.select([sock], [], [], timeout)
        if ready_socks:
            message, address = sock.recvfrom(buffer_size)
            data_str = message.decode()
            print(f"[network_listener] Message reçu de {address}: {data_str}")
            # On place la donnée dans la queue
            received_messages.put(data_str)
        else:
            # Aucun message dans le délai imparti => on continue la boucle
            pass

def start_network_listener(port=5005):
    """
    Lance le thread de réception en arrière-plan (daemon).
    """
    listener_thread = threading.Thread(target=network_listener, args=(port,))
    listener_thread.daemon = True  # le thread s'arrêtera en même temps que le programme principal
    listener_thread.start()
