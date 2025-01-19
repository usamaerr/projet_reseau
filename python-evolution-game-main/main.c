#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>

#define BUFFER_SIZE 1024

// Helper function to set a socket to non-blocking mode
void set_nonblocking(int sock) {
    int flags = fcntl(sock, F_GETFL, 0);
    fcntl(sock, F_SETFL, flags | O_NONBLOCK);
}

int main() {
    int recv_port_python, send_port_python, recv_port_c, send_port_c;
    char buffer[BUFFER_SIZE];
    struct sockaddr_in recv_addr_python, send_addr_python, recv_addr_c, send_addr_c, sender_addr;
    socklen_t addr_len = sizeof(struct sockaddr_in);

    // Demande des ports à l'utilisateur
    printf("Port pour recevoir des messages de Python : ");
    scanf("%d", &recv_port_python);
    printf("Port pour envoyer des messages à Python : ");
    scanf("%d", &send_port_python);
    printf("Port pour recevoir des messages du programme C : ");
    scanf("%d", &recv_port_c);
    printf("Port pour envoyer des messages au programme C : ");
    scanf("%d", &send_port_c);

    // Création des sockets
    int sock_python = socket(AF_INET, SOCK_DGRAM, 0);
    int sock_c = socket(AF_INET, SOCK_DGRAM, 0);

    if (sock_python < 0 || sock_c < 0) {
        perror("Erreur lors de la création des sockets");
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse pour recevoir de Python
    memset(&recv_addr_python, 0, sizeof(recv_addr_python));
    recv_addr_python.sin_family = AF_INET;
    recv_addr_python.sin_port = htons(recv_port_python);
    recv_addr_python.sin_addr.s_addr = INADDR_ANY;

    if (bind(sock_python, (struct sockaddr *)&recv_addr_python, sizeof(recv_addr_python)) < 0) {
        perror("Erreur de binding pour Python");
        close(sock_python);
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse pour envoyer à Python
    memset(&send_addr_python, 0, sizeof(send_addr_python));
    send_addr_python.sin_family = AF_INET;
    send_addr_python.sin_port = htons(send_port_python);
    send_addr_python.sin_addr.s_addr = inet_addr("127.0.0.1");

    // Configuration de l'adresse pour recevoir de C
    memset(&recv_addr_c, 0, sizeof(recv_addr_c));
    recv_addr_c.sin_family = AF_INET;
    recv_addr_c.sin_port = htons(recv_port_c);
    recv_addr_c.sin_addr.s_addr = INADDR_ANY;

    if (bind(sock_c, (struct sockaddr *)&recv_addr_c, sizeof(recv_addr_c)) < 0) {
        perror("Erreur de binding pour C");
        close(sock_c);
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse pour envoyer à C
    memset(&send_addr_c, 0, sizeof(send_addr_c));
    send_addr_c.sin_family = AF_INET;
    send_addr_c.sin_port = htons(send_port_c);
    send_addr_c.sin_addr.s_addr = inet_addr("127.0.0.1");

    // Mettre les sockets en mode non bloquant
    set_nonblocking(sock_python);
    set_nonblocking(sock_c);

    printf("En écoute sur les ports suivants :\n");
    printf("  Python -> Recevoir : %d, Envoyer : %d\n", recv_port_python, send_port_python);
    printf("  C      -> Recevoir : %d, Envoyer : %d\n", recv_port_c, send_port_c);

    // Boucle principale avec `select()`
    while (1) {
        fd_set readfds;
        FD_ZERO(&readfds);

        // Ajouter les sockets au set
        FD_SET(sock_python, &readfds);
        FD_SET(sock_c, &readfds);

        int max_fd = (sock_python > sock_c) ? sock_python : sock_c;

        // Attendre une activité sur une des sockets
        int activity = select(max_fd + 1, &readfds, NULL, NULL, NULL);

        if (activity < 0) {
            perror("Erreur avec select()");
            continue;
        }

        // Vérifier si une activité est présente sur la socket Python
        if (FD_ISSET(sock_python, &readfds)) {
            ssize_t recv_len = recvfrom(sock_python, buffer, BUFFER_SIZE - 1, 0, (struct sockaddr *)&sender_addr, &addr_len);
            if (recv_len > 0) {
                buffer[recv_len] = '\0';
                printf("[Python] Message reçu : %s\n", buffer);

                // Envoyer le message au programme C
                ssize_t send_len = sendto(sock_c, buffer, strlen(buffer), 0, (struct sockaddr *)&send_addr_c, addr_len);
                if (send_len < 0) {
                    perror("Erreur d'envoi vers C");
                } else {
                    printf("[Python -> C] Message relayé : %s\n", buffer);
                }
            }
        }

        // Vérifier si une activité est présente sur la socket C
        if (FD_ISSET(sock_c, &readfds)) {
            ssize_t recv_len = recvfrom(sock_c, buffer, BUFFER_SIZE - 1, 0, (struct sockaddr *)&sender_addr, &addr_len);
            if (recv_len > 0) {
                buffer[recv_len] = '\0';
                printf("[C] Message reçu : %s\n", buffer);

                // Envoyer le message au programme Python
                ssize_t send_len = sendto(sock_python, buffer, strlen(buffer), 0, (struct sockaddr *)&send_addr_python, addr_len);
                if (send_len < 0) {
                    perror("Erreur d'envoi vers Python");
                } else {
                    printf("[C -> Python] Message relayé : %s\n", buffer);
                }
            }
        }
    }

    close(sock_python);
    close(sock_c);

    return 0;
}