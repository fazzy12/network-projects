import socket

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen(5)

print(f"Server is running at http://{HOST}:{PORT}")

print("Press Ctrl+C to stop.\n")


while True:
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address}")

    raw_data = client_socket.recv(4096)
    request_text = raw_data.decode()


    lines = request_text.split("\r\n")
    request_line = lines[0]

    parts = request_line.split(" ")
    method = parts[0]
    path = parts[1]
    version = parts[2]

    print(f" method: {method}")
    print(f" path: {path}")
    print(f" version: {version}")

    header = {}
    for line in lines[1:]:
        if line == "":
            break
        key, value = line.split(": ", 1)
        header[key] = value

    body_text = f"Hello! You requested the path: {path}\n"
    body_bytes = body_text.encode()

    status_line = "HTTP/1.1 200 ok"
    response_headers = (
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"Connection: close\r\n"
    )

    response = (
        status_line + "\r\n" + 
        response_headers + 
        "\r\n"
    ).encode() + body_bytes


    client_socket.sendall(response)
    client_socket.close()
    print(" Responded and closed connection.\n")
