import socket

def main():
    listen_port = 12345  # Port to match the sender's `send_port`
    response_message = "Acknowledged: Data received successfully!"

    # Create a socket for listening
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.bind(("0.0.0.0", listen_port))  # Listen on all interfaces

    print(f"Listening on port {listen_port} for incoming data...")

    while True:
        # Receive data
        data, addr = listen_socket.recvfrom(65536)
        print(f"Message received from {addr}:\n{data.decode('utf-8')}")

        # Send a response back
        listen_socket.sendto(response_message.encode('utf-8'), addr)
        print(f"Response sent to {addr}:\n{response_message}")

if __name__ == "__main__":
    main()
