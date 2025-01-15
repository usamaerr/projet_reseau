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

    
}



