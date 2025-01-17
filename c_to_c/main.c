#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>

// Function to set a socket to non-blocking mode
void set_nonblocking(int sock) {
    int flags = fcntl(sock, F_GETFL, 0);
    fcntl(sock, F_SETFL, flags | O_NONBLOCK);
}

int main() {
    int port = 2222;
    char buffer[1024];
    struct sockaddr_in addr, broadcast_addr;
    socklen_t addr_len = sizeof(struct sockaddr_in);

    // Create the UDP socket
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Allow multiple sockets to use the same port
    int reuse = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) {
        perror("Failed to set SO_REUSEADDR");
        close(sock);
        exit(EXIT_FAILURE);
    }

    // Set the socket to allow broadcasting
    int broadcast_enable = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &broadcast_enable, sizeof(broadcast_enable)) < 0) {
        perror("Failed to enable broadcast");
        close(sock);
        exit(EXIT_FAILURE);
    }

    // Bind the socket to the specified port
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = INADDR_ANY; // Listen on all interfaces

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("Binding failed");
        close(sock);
        exit(EXIT_FAILURE);
    }

    // Configure the broadcast address
    memset(&broadcast_addr, 0, sizeof(broadcast_addr));
    broadcast_addr.sin_family = AF_INET;
    broadcast_addr.sin_port = htons(port);
    broadcast_addr.sin_addr.s_addr = inet_addr("255.255.255.255");

    // Set the socket to non-blocking mode
    set_nonblocking(sock);

    printf("Game started! Listening for messages and ready to send.\n");

    while (1) {
        // Non-blocking receive
        ssize_t recv_len = recvfrom(sock, buffer, sizeof(buffer) - 1, 0, (struct sockaddr *)&addr, &addr_len);
        if (recv_len > 0) {
            /**
             * @brief Null-terminate the received data and print the received message.
             * 
             * @details This section of code ensures that the received data is properly
             * null-terminated to avoid buffer overflow issues and then prints the message
             * received from the network.
             */

             /**
             * @brief Prompt the user for input and send it as a broadcast message.
             * 
             * @details This section of code prompts the user to enter their move, reads
             * the input using fgets, removes the newline character, and sends the input
             * as a broadcast message to the specified address. If the message fails to
             * send, an error message is printed. Otherwise, it confirms that the message
             * was sent successfully.
             */

             /**
             * @brief Sleep for 100 milliseconds to avoid busy-waiting.
             * 
             * @details This section of code introduces a delay of 100 milliseconds to
             * prevent the program from continuously running in a busy-wait loop, which
             * can consume unnecessary CPU resources.
             */
            buffer[recv_len] = '\0'; // Null-terminate the received data
            printf("\nMessage received: %s\n", buffer);
        }

        // Prompt the user for input
        printf("Your move: ");
        fflush(stdout);

        // Use fgets to read user input
        if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
            buffer[strcspn(buffer, "\n")] = '\0'; // Remove the newline character

            // Send the input as a broadcast message
            ssize_t send_len = sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr *)&broadcast_addr, addr_len);
            if (send_len < 0) {
                perror("Failed to send message");
            } else {
                printf("Message sent: %s\n", buffer);
            }
        }

        usleep(100000); // Avoid busy-waiting by sleeping for 100ms
    }

    // Close the socket
    close(sock);
    return 0;
}
