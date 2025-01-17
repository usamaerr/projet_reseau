import socket
import select

def main():
    # Configurations
    send_ip = "127.0.0.1"  # IP of the receiving machine (can be localhost for local tests)
    send_port = 12345         # Port to send data to
    listen_port = 12346       # Port to listen for incoming data
    filename = "distant.txt"     # ASCII file to send

    # Create a socket for sending
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Create a socket for listening
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.bind(("0.0.0.0", listen_port))  # Listen on all interfaces

    print(f"Python listening on port {listen_port} for incoming data...")

    # Load the ASCII data to send
    try:
        with open(filename, 'r') as file:
            ascii_data = file.read()
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return

    # Send the data to the target
    send_socket.sendto(ascii_data.encode('utf-8'), (send_ip, send_port))
    print(f"File {filename} sent to {send_ip}:{send_port}:\n{ascii_data}")

    # Listen for responses
    while True:
        # Use select to check if the listening socket has data
        read_sockets, _, _ = select.select([listen_socket], [], [], 5)  # Timeout of 5 seconds

        for sock in read_sockets:
            if sock == listen_socket:
                data, addr = listen_socket.recvfrom(65536)  # Receive data
                print(f"Response received from {addr}:\n{data.decode('utf-8')}")
                return  # Exit after receiving one response

if __name__ == "__main__":
    main()
