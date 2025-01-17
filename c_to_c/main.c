/**
 * @file main.c
 * @brief A simple UDP broadcast and receive program.
 *
 * This program allows the user to send and receive messages over UDP using broadcast.
 * It sets up a socket for receiving messages on a specified port and another for sending
 * messages to a broadcast address on a different port.
 *
 * The socket is set to non-blocking mode to allow simultaneous sending and receiving of messages.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>

/**
 * @brief Set a socket to non-blocking mode.
 *
 * @param sock The socket file descriptor.
 */
void set_nonblocking(int sock) {
    int flags = fcntl(sock, F_GETFL, 0); ///< Get the current socket flags.
    fcntl(sock, F_SETFL, flags | O_NONBLOCK); ///< Set the socket to non-blocking mode.
}

int main() {
    int send_port, recv_port; ///< Ports for sending and receiving messages.
    char buffer[1024]; ///< Buffer for storing messages.
    struct sockaddr_in recv_addr, broadcast_addr, sender_addr; ///< Socket addresses for receiving, broadcasting, and sender.
    socklen_t addr_len = sizeof(struct sockaddr_in); ///< Length of the socket address structure.

    // Input ports for sending and receiving
    printf("Enter the port to use for receiving messages: ");
    scanf("%d", &recv_port); ///< Get the receiving port from the user.
    printf("Enter the port to use for sending messages: ");
    scanf("%d", &send_port); ///< Get the sending port from the user.

    // Create the socket
    int sock = socket(AF_INET, SOCK_DGRAM, 0); ///< Create a UDP socket.
    if (sock < 0) {
        perror("Socket creation failed"); ///< Print error message if socket creation fails.
        exit(EXIT_FAILURE); ///< Exit the program with failure status.
    }

    // Enable broadcast on the socket
    int broadcast_enable = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &broadcast_enable, sizeof(broadcast_enable)) < 0) {
        perror("Failed to enable broadcast"); ///< Print error message if enabling broadcast fails.
        close(sock); ///< Close the socket.
        exit(EXIT_FAILURE); ///< Exit the program with failure status.
    }

    // Bind the socket to the receiving port
    memset(&recv_addr, 0, sizeof(recv_addr)); ///< Clear the receiving address structure.
    recv_addr.sin_family = AF_INET; ///< Set the address family to AF_INET.
    recv_addr.sin_port = htons(recv_port); ///< Set the receiving port.
    recv_addr.sin_addr.s_addr = INADDR_ANY; ///< Accept messages from any address.

    if (bind(sock, (struct sockaddr *)&recv_addr, sizeof(recv_addr)) < 0) {
        perror("Binding failed"); ///< Print error message if binding fails.
        close(sock); ///< Close the socket.
        exit(EXIT_FAILURE); ///< Exit the program with failure status.
    }

    // Configure the broadcast address for sending
    memset(&broadcast_addr, 0, sizeof(broadcast_addr)); ///< Clear the broadcast address structure.
    broadcast_addr.sin_family = AF_INET; ///< Set the address family to AF_INET.
    broadcast_addr.sin_port = htons(send_port); ///< Set the sending port.
    broadcast_addr.sin_addr.s_addr = inet_addr("255.255.255.255"); ///< Set the broadcast address.

    set_nonblocking(sock); ///< Set the socket to non-blocking mode.

    printf("Game started! Listening for messages on port %d and broadcasting to port %d.\n", recv_port, send_port);

    while (1) {
        // Non-blocking receive
        ssize_t recv_len = recvfrom(sock, buffer, sizeof(buffer) - 1, 0, (struct sockaddr *)&sender_addr, &addr_len); ///< Receive a message.
        if (recv_len > 0) {
            buffer[recv_len] = '\0'; ///< Null-terminate the received message.

            // Filter out messages sent by itself
            if (ntohs(sender_addr.sin_port) != recv_port) {
                printf("\nMessage received: %s\n", buffer); ///< Print the received message.
            }
        }

        // Prompt the user for input
        printf("Your move: ");
        fflush(stdout); ///< Flush the output buffer.

        if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
            buffer[strcspn(buffer, "\n")] = '\0'; ///< Remove the newline character.

            // Send the input as a broadcast message
            ssize_t send_len = sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr *)&broadcast_addr, addr_len); ///< Send the message.
            if (send_len < 0) {
                perror("Failed to send message"); ///< Print error message if sending fails.
            } else {
                printf("Message broadcasted: %s\n", buffer); ///< Print the broadcasted message.
            }
        }

        usleep(100000); ///< Avoid busy-waiting by sleeping for 100 milliseconds.
    }

    close(sock); ///< Close the socket.
    return 0; ///< Return success status.
}
