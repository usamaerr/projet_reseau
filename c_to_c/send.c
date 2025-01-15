#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define BROADCAST_ADDR "255.255.255.255"  // Adresse de broadcast

int main() {
    int sock;
    struct sockaddr_in broadcast_addr;
    int optval = 1;
    char message[1024];
    int port;

    // Demander à l'utilisateur de saisir le port
    printf("Entrez le port à utiliser : ");
    scanf("%d", &port);

    // Création du socket UDP
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("Erreur lors de la création du socket");
        exit(EXIT_FAILURE);
    }

    // Autoriser l'envoi de paquets en broadcast
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &optval, sizeof(optval)) < 0) {
        perror("Erreur lors de l'activation du broadcast");
        close(sock);
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse de broadcast
    memset(&broadcast_addr, 0, sizeof(broadcast_addr));
    broadcast_addr.sin_family = AF_INET;
    broadcast_addr.sin_port = htons(port);  // Utilisation du port entré par l'utilisateur
    broadcast_addr.sin_addr.s_addr = inet_addr(BROADCAST_ADDR);

    // Boucle pour envoyer des messages
    while (1) {
        printf("Entrez un message à envoyer : ");
        fgets(message, sizeof(message), stdin);  // Pour permettre à l'utilisateur d'entrer le message
        message[strcspn(message, "\n")] = '\0'; // Retirer le saut de ligne après l'entrée

        if (sendto(sock, message, strlen(message), 0, (struct sockaddr *)&broadcast_addr, sizeof(broadcast_addr)) < 0) {
            perror("Erreur lors de l'envoi du message");
        }
    }

    close(sock);
    return 0;
}
