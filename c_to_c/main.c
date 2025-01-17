#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>

// Helper function to set a socket to non-blocking mode
void set_nonblocking(int sock) {
    int flags = fcntl(sock, F_GETFL, 0);
    fcntl(sock, F_SETFL, flags | O_NONBLOCK);
}

int main() {
    int recv_port, send_port;
    char buffer[1024];
    struct sockaddr_in recv_addr, relay_addr, sender_addr;
    socklen_t addr_len = sizeof(struct sockaddr_in);

    // Ports pour recevoir et relayer
    printf("Port pour recevoir des messages (du processus Python) : ");
    scanf("%d", &recv_port);
    printf("Port pour relayer les messages (au second processus) : ");
    scanf("%d", &send_port);

    // Création du socket
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("Échec de la création du socket");
        exit(EXIT_FAILURE);
    }

    // Configuration pour recevoir sur recv_port
    memset(&recv_addr, 0, sizeof(recv_addr));
    recv_addr.sin_family = AF_INET;
    recv_addr.sin_port = htons(recv_port);
    recv_addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(sock, (struct sockaddr *)&recv_addr, sizeof(recv_addr)) < 0) {
        perror("Échec du binding");
        close(sock);
        exit(EXIT_FAILURE);
    }

    // Adresse pour relayer les messages
    memset(&relay_addr, 0, sizeof(relay_addr));
    relay_addr.sin_family = AF_INET;
    relay_addr.sin_port = htons(send_port);
    relay_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // Remplacez par l'adresse réelle si nécessaire

    set_nonblocking(sock);

    printf("En écoute sur le port %d pour relayer vers le port %d.\n", recv_port, send_port);

    while (1) {
        // Réception non bloquante
        ssize_t recv_len = recvfrom(sock, buffer, sizeof(buffer) - 1, 0, (struct sockaddr *)&sender_addr, &addr_len);
        if (recv_len > 0) {
            buffer[recv_len] = '\0'; // Ajouter un terminateur à la chaîne
            printf("Message reçu : %s\n", buffer);

            // Relayer le message au second processus
            ssize_t send_len = sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr *)&relay_addr, addr_len);
            if (send_len < 0) {
                perror("Échec de l'envoi du message");
            } else {
                printf("Message relayé : %s\n", buffer);
            }
        }

        usleep(100000); // Éviter le busy-waiting
    }

    close(sock);
    return 0;
}