import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080

BUFFER_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_HOST, SERVER_PORT))

server.listen(5)
print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

connection, address = server.accept()
print(f"[*] Accepted connection from {address[0]}:{address[1]}")

data = connection.recv(BUFFER_SIZE)
message = data.decode("utf-8")

if message.startswith("FILE_REQUEST:"):
    filename = message.split(":", 1)[1]
    print(f"Zahtjev za prijenos datoteke: {filename}")

    choice = input("Accept file transfer? (y/n): ")

    if choice.lower() == "y":
        connection.sendall(f"File sharing accepted: {filename}".encode("utf-8"))
        print("File transfer accepted.")

    else:
        connection.sendall(f"File sharing rejected: {filename}".encode("utf-8"))
        print("File transfer rejected.")

connection.close()
server.close()