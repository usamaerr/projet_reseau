import subprocess
import os

def launch_terminal(command):
    """Lance une commande dans un nouveau terminal."""
    terminal_command = [
        "gnome-terminal", "--", "bash", "-c", f"{command}; exec bash"
    ]
    subprocess.Popen(terminal_command)

def main():
    # Chemin des scripts et exécutables
    c_to_py_script = os.path.abspath("c_to_py.py")
    py_to_c_script = os.path.abspath("py_to_c.py")
    executable = os.path.abspath("exee")

    # Vérifie l'existence des fichiers requis
    for path in [c_to_py_script, py_to_c_script, executable]:
        if not os.path.exists(path):
            print(f"Erreur : Le fichier {path} est introuvable.")
            return

    # Commande pour le premier terminal (lancer c_to_py.py)
    launch_terminal(f"python3 {c_to_py_script}")

    # Commande pour le deuxième terminal (lancer l'exécutable avec les premiers ports)
    inputs_1 = """echo -e '5004\n5005\n5003\n5002' | """
    launch_terminal(f"{inputs_1} {executable}")

    # Commande pour le troisième terminal (lancer l'exécutable avec les deuxièmes ports)
    inputs_2 = """echo -e '5001\n5000\n5002\n5003' | """
    launch_terminal(f"{inputs_2} {executable}")

    # Commande pour le quatrième terminal (lancer py_to_c.py)
    launch_terminal(f"python3 {py_to_c_script}")

if __name__ == "__main__":
    main()
