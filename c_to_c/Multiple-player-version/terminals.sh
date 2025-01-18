#!/bin/bash

# Ports de réception pour les 10 terminaux
ports=(5001 5002 5003 5004 5005 5006 5007 5008 5009 5010)

# Lancer les 10 terminaux
for i in "${!ports[@]}"; do
    recv_port=${ports[$i]}
    send_ports=("${ports[@]}")  # Copie de la liste des ports
    unset "send_ports[$i]"      # Supprimer le port de réception actuel
    send_ports=("${send_ports[@]}")  # Réindexer le tableau

    # Ouvrir un nouveau terminal et exécuter le programme
    gnome-terminal -- bash -c "./tuyauterie10 $recv_port ${send_ports[*]}; exec bash"
done