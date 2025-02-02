Projet Réseau

Description du Projet

Ce projet permet une communication réseau entre deux joueurs en utilisant un programme écrit en C et une interface graphique en Python.

Instructions pour Lancer la Première Version entre Deux Joueurs

1. Préparation des programmes C

Ouvrez deux terminaux pour exécuter deux instances du programme C.

Dans chaque terminal, compilez le fichier main.c avec la commande suivante :

  gcc main.c -o main

Lancez le programme dans chaque terminal :

Terminal 1 :

  ./main

Ports utilisés :

  Réception des messages Python : 5001

  Envoi des messages vers Python : 5000

  Réception des messages du programme C : 5002

  Envoi des messages au programme C : 5003

Terminal 2 :

  ./main

Ports utilisés :

  Réception des messages Python : 5004

  Envoi des messages vers Python : 5005

  Réception des messages du programme C : 5003

  Envoi des messages au programme C : 5002

2. Lancement des programmes Python

Ouvrez deux nouveaux terminaux pour exécuter les programmes Python avec une interface graphique.

Dans chaque terminal, exécutez le programme Python :

Terminal 3 :

  python3 main.py

Après le lancement :

  Cliquez sur Play dans l'interface graphique.

  Entrez un nom de joueur unique (différent de celui du second joueur).

Revenez au terminal et configurez les ports :

  Port de réception : 5000

  Port d'envoi : 5001

Terminal 4 :

  python3 main.py

Après le lancement :

  Cliquez sur Play dans l'interface graphique.

  Entrez un nom de joueur unique (différent de celui du premier joueur).

Revenez au terminal et configurez les ports :

  Port de réception : 5005

  Port d'envoi : 5004

