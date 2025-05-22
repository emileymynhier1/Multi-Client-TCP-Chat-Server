# client.py
# Name: Emily Mynhier
# Course: CSC138 Spring 2025
# Date: April 2025
# Description: Client-side chat program. Sends commands to the server and displays messages.

import socket
import sys
import threading
import select

# Continuously listen for server messages and print them
def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break

# Validate command-line usage
if len(sys.argv) != 3:
    print("Usage: python3 client.py <hostname> <port>")
    sys.exit(1)

# Get hostname and port from command-line
hostname = sys.argv[1]
port = int(sys.argv[2])

# Set up TCP socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((hostname, port))

# Start thread to receive messages from server
receiver_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
receiver_thread.start()

# Continuously get user input and send to server
try:
    while True:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            msg = sys.stdin.readline().strip()
        else:
            msg = input()
        if msg:
            client_socket.sendall(f"{msg}\n".encode())
        if msg.startswith("QUIT"):
            break
except KeyboardInterrupt:
    pass
finally:
    client_socket.close()
