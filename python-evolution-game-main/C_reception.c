/*#include <stdio.h>
#include <stdlib.h>

int main() {
    char buffer[1024];

    // Lire depuis l'entrée standard
    if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
        printf("Message reçu depuis Python : %s\n", buffer);
    } else {
        fprintf(stderr, "Erreur de lecture sur stdin\n");
    }

    return 0;
    }*/

/*code de test
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


    
}*/




#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 12345        // Port d'écoute
#define BUFFER_SIZE 65536 // Taille maximale pour un message volumineux

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
    servaddr.sin_addr.s_addr = INADDR_ANY;      // Écouter sur toutes les interfaces
    servaddr.sin_port = htons(PORT);           // Port d'écoute

    // Associer le socket à l'adresse et au port
    if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("Erreur de liaison (bind)");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("En attente de messages ASCII...\n");

    // Recevoir le message ASCII
    len = sizeof(cliaddr);
    int n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&cliaddr, &len);
    if (n < 0) {
        perror("Erreur lors de la réception");
    } else {
        buffer[n] = '\0'; // Terminer la chaîne reçue
        printf("Message ASCII reçu :\n%s\n", buffer);
    }

    close(sockfd);
    return 0;
}




