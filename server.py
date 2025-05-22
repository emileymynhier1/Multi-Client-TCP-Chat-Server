# server.py
# Name: Emily Mynhier
# Course: CSC138 Spring 2025
# Date: April 2025
# Description: TCP server for multi-client chat. Supports JOIN, LIST, MESG, BCST, LOG, QUIT.

import socket
import threading
import sys
import datetime

# Max number of registered users
MAX_CLIENTS = 10

# Dictionary to store username essentially socket
clients = {}

# Dictionary to track client logs
client_logs = {}

# Lock for thread-safe operations
lock = threading.Lock()

# Broadcast a message to all other connected users
def broadcast(sender_username, message):
    for username, conn in clients.items():
        if username != sender_username:
            try:
                conn.sendall(f"{sender_username} {message}\n".encode())
            except:
                continue

# Send a private message to a specific recipient
def send_private(sender, recipient, message):
    if recipient in clients:
        try:
            clients[recipient].sendall(f"{sender} {message}\n".encode())
            return True
        except:
            return False
    return False

# Save a message to the users log file
def save_log(username, log_entry):
    with open(f"log_{username}.txt", "a") as f:
        f.write(log_entry + "\n")

# Handle interaction with a single client
def handle_client(conn, addr):
    print(f"Connected with {addr}")
    username = None

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            tokens = data.strip().split(" ", 2)
            command = tokens[0]

            if command == "JOIN":
                if len(tokens) < 2:
                    conn.sendall("Usage: JOIN <username>\n".encode())
                    continue
                with lock:
                    if username:
                        conn.sendall("Already joined.\n".encode())
                        continue
                    if tokens[1] in clients:
                        conn.sendall("Username already taken. Try another.\n".encode())
                        continue
                    if len(clients) >= MAX_CLIENTS:
                        conn.sendall("Too Many Users\n".encode())
                        break
                    username = tokens[1]
                    clients[username] = conn
                    client_logs[username] = []
                    conn.sendall(f"{username} joined!Connected to server!\n".encode())
                    print(f"{username} Joined the Chatroom")
                    broadcast("Server", f"{username} joined!")

            # LIST command
            elif command == "LIST":
                if username:
                    userlist = ",".join(clients.keys())
                    conn.sendall(f"{userlist}\n".encode())
                else:
                    conn.sendall("JOIN required.\n".encode())

            # MESG command
            elif command == "MESG":
                if len(tokens) < 3:
                    conn.sendall("Usage: MESG <user> <message>\n".encode())
                    continue
                if not username:
                    conn.sendall("Unregistered User. Use JOIN first.\n".encode())
                    continue
                recipient = tokens[1]
                msg = tokens[2]
                timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                log_entry = f"{timestamp} INFO: Message sent by {username} to {recipient} - \"{msg}\""
                if send_private(username, recipient, msg):
                    save_log(username, log_entry)
                    save_log(recipient, log_entry)
                else:
                    conn.sendall("Unknown Recipient.\n".encode())

            # BCST command
            elif command == "BCST":
                if not username:
                    conn.sendall("Unregistered User. Use JOIN first.\n".encode())
                    continue
                msg = tokens[1] if len(tokens) > 1 else ""
                if len(tokens) == 3:
                    msg = "Broadcasting: " + tokens[1] + " " + tokens[2]
                timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                log_entry = f"{timestamp} INFO: Broadcast by {username} - \"{msg}\""
                broadcast(username, msg)
                save_log(username, log_entry)

            # LOG command
            elif command == "LOG":
                if not username:
                    conn.sendall("Unregistered User. Use JOIN first.\n".encode())
                    continue
                try:
                    with open(f"log_{username}.txt", "r") as f:
                        conn.sendall(f.read().encode())
                except FileNotFoundError:
                    conn.sendall("No log found.\n".encode())

            # QUIT command
            elif command == "QUIT":
                break

            # Unknown command
            else:
                conn.sendall("Unknown Message.\n".encode())

        except:
            break

    # Client disconnected - cleanup
    with lock:
        if username and username in clients:
            print(f"{username} left")
            del clients[username]
            broadcast("Server", f"{username} left!")
    conn.close()

# Start server and accept incoming connections
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 server.py <svr_port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(10)
    print("The Chat Server Started")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
