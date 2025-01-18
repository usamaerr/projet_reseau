#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>

#define MAX_TERMINALS 10
#define BUFFER_SIZE 1024

/**
 * @brief Set a socket to non-blocking mode.
 *
 * @param sock The socket file descriptor.
 */
void set_nonblocking(int sock) {
    int flags = fcntl(sock, F_GETFL, 0); ///< Get the current socket flags.
    fcntl(sock, F_SETFL, flags | O_NONBLOCK); ///< Set the socket to non-blocking mode.
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <recv_port> <send_port1> <send_port2> ... <send_portN>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    // Port de réception
    int recv_port = atoi(argv[1]); ///< Port de réception fixe.

    // Liste des ports d'envoi
    int send_ports[MAX_TERMINALS];
    int num_send_ports = argc - 2;
    for (int i = 0; i < num_send_ports; i++) {
        send_ports[i] = atoi(argv[i + 2]);
    }

    // Message statique propre à ce terminal
    char static_message[BUFFER_SIZE];
    snprintf(static_message, sizeof(static_message), "Hello from Terminal on port %d", recv_port);

    char buffer[BUFFER_SIZE]; ///< Buffer pour stocker les messages.
    struct sockaddr_in recv_addr, send_addrs[MAX_TERMINALS], sender_addr; ///< Adresses pour la réception, l'envoi et l'expéditeur.
    socklen_t addr_len = sizeof(struct sockaddr_in); ///< Longueur de la structure d'adresse.

    // Créer le socket
    int sock = socket(AF_INET, SOCK_DGRAM, 0); ///< Créer un socket UDP.
    if (sock < 0) {
        perror("Socket creation failed"); ///< Afficher un message d'erreur si la création du socket échoue.
        exit(EXIT_FAILURE); ///< Quitter le programme avec un statut d'échec.
    }

    // Lier le socket au port de réception
    memset(&recv_addr, 0, sizeof(recv_addr)); ///< Initialiser la structure d'adresse de réception.
    recv_addr.sin_family = AF_INET; ///< Définir la famille d'adresses à AF_INET.
    recv_addr.sin_port = htons(recv_port); ///< Définir le port de réception.
    recv_addr.sin_addr.s_addr = INADDR_ANY; ///< Accepter les messages de n'importe quelle adresse.

    if (bind(sock, (struct sockaddr *)&recv_addr, sizeof(recv_addr)) < 0) {
        perror("Binding failed"); ///< Afficher un message d'erreur si la liaison échoue.
        close(sock); ///< Fermer le socket.
        exit(EXIT_FAILURE); ///< Quitter le programme avec un statut d'échec.
    }

    // Configurer les adresses d'envoi
    for (int i = 0; i < num_send_ports; i++) {
        memset(&send_addrs[i], 0, sizeof(send_addrs[i])); ///< Initialiser la structure d'adresse d'envoi.
        send_addrs[i].sin_family = AF_INET; ///< Définir la famille d'adresses à AF_INET.
        send_addrs[i].sin_port = htons(send_ports[i]); ///< Définir le port d'envoi.
        send_addrs[i].sin_addr.s_addr = inet_addr("127.0.0.1"); ///< Définir l'adresse de destination (localhost).
    }

    set_nonblocking(sock); ///< Passer le socket en mode non-bloquant.

    printf("Terminal started! Listening for messages on port %d and sending to %d ports.\n", recv_port, num_send_ports);
    printf("Static message: %s\n", static_message);

    while (1) {
        // Réception non-bloquante
        ssize_t recv_len = recvfrom(sock, buffer, sizeof(buffer) - 1, 0, (struct sockaddr *)&sender_addr, &addr_len); ///< Recevoir un message.
        if (recv_len > 0) {
            buffer[recv_len] = '\0'; ///< Terminer le message reçu par un caractère nul.

            // Filtrer les messages envoyés par ce terminal
            if (ntohs(sender_addr.sin_port) != recv_port) {
                printf("\nMessage received from %s:%d: %s\n", inet_ntoa(sender_addr.sin_addr), ntohs(sender_addr.sin_port), buffer); ///< Afficher le message reçu.
            }
        }

        // Envoyer le message statique à tous les autres terminaux
        for (int i = 0; i < num_send_ports; i++) {
            ssize_t send_len = sendto(sock, static_message, strlen(static_message), 0, (struct sockaddr *)&send_addrs[i], addr_len); ///< Envoyer le message.
            if (send_len < 0) {
                perror("Failed to send message"); ///< Afficher un message d'erreur si l'envoi échoue.
            }
        }

        printf("Message sent to all terminals: %s\n", static_message); ///< Afficher le message envoyé.

        usleep(1000000); ///< Attendre 1 seconde avant de renvoyer un message.
    }

    close(sock); ///< Fermer le socket.
    return 0; ///< Retourner un statut de succès.
}