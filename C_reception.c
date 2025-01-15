#include <stdio.h>
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
}
