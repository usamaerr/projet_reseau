import sys

def send_message_to_stdout():
    # Message à envoyer
    message = "hello world"
    
    # Écrire le message sur la sortie standard
    sys.stdout.write(message + "\n")
    sys.stdout.flush()  # S'assurer que le message est immédiatement envoyé

if __name__ == "__main__":
    send_message_to_stdout()
