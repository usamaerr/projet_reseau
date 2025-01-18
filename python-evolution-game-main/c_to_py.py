import socket

recv_port = 5005  # Port to receive messages
buffer_size = 1024

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", recv_port))

print(f"Python program started! Listening on port {recv_port}...")

while True:
    message, address = sock.recvfrom(buffer_size)
    print(f"Message received from {address}: {message.decode()}")