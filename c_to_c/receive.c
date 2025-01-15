#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define BUF_SIZE 1024

int main() {
    int sock;
    struct sockaddr_in server_addr;
    char buffer[BUF_SIZE];
    int port;

    // Demander à l'utilisateur de saisir le port
    printf("Entrez le port à écouter : ");
    scanf("%d", &port);

    // Création du socket UDP
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("Erreur lors de la création du socket");
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse du serveur (toute adresse du réseau)
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;  // Accepter les messages de n'importe quelle adresse
    server_addr.sin_port = htons(port);  // Utilisation du port entré par l'utilisateur

    // Lier le socket à l'adresse et au port
    if (bind(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Erreur lors du bind");
        close(sock);
        exit(EXIT_FAILURE);
    }

    printf("En attente de messages sur le port %d...\n", port);

    // Réception des messages
    while (1) {
        int len = sizeof(server_addr);
        int n = recvfrom(sock, buffer, BUF_SIZE, 0, (struct sockaddr *)&server_addr, &len);
        if (n < 0) {
            perror("Erreur lors de la réception");
            continue;
        }
        buffer[n] = '\0';  // Terminer la chaîne
        printf("Message reçu : %s\n", buffer);
    }

    close(sock);
    return 0;
}
