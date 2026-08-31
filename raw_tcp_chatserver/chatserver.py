"""
    chat_server.py — raw-socket TCP chat server (no frameworks, stdlib only)

"""

import socket
import threading

# listen on all network interfaces
HOST = "0.0.0.0"   
PORT = 5050
clients = []


def braodcast(message, sender_file=None):
    """Send `message` to every connected client except the sender."""
    
    for file, name in clients:
        if file is not sender_file:
            try:
                file.write(message + "\n")
                  # to make sure it actually goes out over the network
                file.flush()
            except OSError:
                pass

def handle_client(conn, addr):
    file =conn.makefile("rw")
    
    
    username = file.readline().strip()
    print(f"[+] {username} connected from {addr}")
    
    
    clients.append((file, username))
    braodcast(f"* {username} joined the chat", sender_file=file)
    
    try:
        while True:
            line = file.readline()
            if line == "":
                break
            message = line.strip()
            print(f"{username}: {message}")
            braodcast(f"{username}: {message}", sender_file=file)
    finally:
        clients.remove((file, username))
        print(f"[-] {username} disconnected")
        braodcast(f"* {username} left the chat")
        conn.close()

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"Server is listerning on {PORT}...")
    
    
    while True:
        conn, addr = server_sock.accept()
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()