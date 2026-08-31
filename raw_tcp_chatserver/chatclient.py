import socket
import threading

HOST = "127.0.0.1"
PORT = 5050

def listen_for_message(file):
    """Runs in the background: prints anything the server sends us."""
    while True:
        line = file.readline()
        if line == "":
            print("server closed connection.")
            break
        print(line.strip())

def main():
    username = input("choose a username: ")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    file = sock.makefile("rw")
    
    
    file.write(username + "\n")
    file.flush()
    
    
    listener = threading.Thread(target=listen_for_message, args=(file,), daemon=True)
    listener.start()
    
    print("Connected! Type a message and press Enter to send.")
    try:
        while True:
            text = input()
            file.write(text + "\n")
            file.flush()
    except (KeyboardInterrupt, EOFError):
        print("Disconnecting.....")
    finally:
        sock.close()

if __name__ == "__main__":
    main()