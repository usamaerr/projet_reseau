#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 12345       // Port d'écoute
#define BUFFER_SIZE 1024 // Taille maximale du buffer

int main() {
    int sockfd;
    char buffer[BUFFER_SIZE];
    struct sockaddr_in servaddr, cliaddr;
    socklen_t len;

    // Créer un socket UDP
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Erreur de création du socket");
        exit(EXIT_FAILURE);
    }

    // Configurer l'adresse et le port
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;              // IPv4
    servaddr.sin_addr.s_addr = INADDR_ANY;      // Accepter les connexions de n'importe où
    servaddr.sin_port = htons(PORT);           // Port d'écoute

    // Associer le socket à l'adresse et au port
    if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("Erreur de liaison (bind)");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("En attente de messages UDP...\n");

    // Boucle pour recevoir les messages
    len = sizeof(cliaddr);
    int n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&cliaddr, &len);
    if (n < 0) {
        perror("Erreur lors de la réception");
    } else {
        buffer[n] = '\0'; // Terminer la chaîne de caractères
        printf("Message reçu : %s\n", buffer);
    }

    close(sockfd);
    return 0;
}
