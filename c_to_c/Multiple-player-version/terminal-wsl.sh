#!/bin/bash

# Ports de réception pour les 10 terminaux
ports=(5001 5002 5003 5004 5005 5006 5007 5008 5009 5010)

# Compiler le programme C (si ce n'est pas déjà fait)
gcc -o joueur joueur.c

# Démarrer une session tmux
tmux new-session -d -s "multi_terminal"

# Lancer les 10 terminaux dans des panneaux tmux
for i in "${!ports[@]}"; do
    recv_port=${ports[$i]}
    send_ports=("${ports[@]}")  # Copie de la liste des ports
    unset "send_ports[$i]"      # Supprimer le port de réception actuel
    send_ports=("${send_ports[@]}")  # Réindexer le tableau

    # Créer un nouveau panneau tmux et exécuter le programme
    if [ $i -eq 0 ]; then
        tmux rename-window -t "multi_terminal" "Terminal $recv_port"
    else
        tmux split-window -v -t "multi_terminal"
        tmux select-layout -t "multi_terminal" tiled
    fi
    tmux send-keys -t "multi_terminal" "./tuyauterie10 $recv_port ${send_ports[*]}" C-m
done

# Attacher la session tmux pour voir les terminaux
tmux attach-session -t "multi_terminal"