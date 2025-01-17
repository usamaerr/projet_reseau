#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>

#define SERVER_IP "127.0.0.1"  // Adresse IP du destinataire (localhost pour ce test)
#define SERVER_PORT 12345      // Port du serveur

int main() {
    int sock;
    struct sockaddr_in server_addr;
    char *message = "Hello from C program!";  // Message à envoyer

    // Créer un socket UDP
    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));

    // Configurer l'adresse du serveur (adresse IP et port)
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    server_addr.sin_addr.s_addr = inet_addr(SERVER_IP);

    // Envoyer le message via UDP
    if (sendto(sock, message, strlen(message), 0, (const struct sockaddr *) &server_addr, sizeof(server_addr)) == -1) {
        perror("Failed to send message");
        close(sock);
        exit(EXIT_FAILURE);
    }

    printf("Message envoyé: %s\n", message);

    // Fermer le socket
    close(sock);
    return 0;
}

