import socket
import os


def receive_all_bytes(connection, size):
    chunks = []
    bytes_received = 0

    while bytes_received < size:
        chunk = connection.recv(min(size - bytes_received, 2048))

        if chunk == b'':
            raise RuntimeError("Socket connection broken")

        chunks.append(chunk)
        bytes_received += len(chunk)

    return b''.join(chunks)


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080

BUFFER_SIZE = 1024
BUFFER_SIZE_FILE = 65536

SAVE_DIR = "received_files"
os.makedirs(SAVE_DIR, exist_ok=True)

BYTE_NUM = 8


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

        size_data = receive_all_bytes(connection, BYTE_NUM)
        file_size = int.from_bytes(size_data, byteorder='big')
        print(f"File size: {file_size} bytes")

        save_path = os.path.join(SAVE_DIR, filename)

        received_size = 0

        with open(save_path, "wb") as file:
            while received_size < file_size:
                chunk_size = min(BUFFER_SIZE_FILE, file_size - received_size)

                data = receive_all_bytes(connection, chunk_size)

                file.write(data)
                received_size += len(data)

                if not data:
                    break

        if received_size == file_size:
            print(f"File '{filename}' successfully received.")
        else:
            print("File transfer incomplete.")

    else:
        connection.sendall(f"File sharing rejected: {filename}".encode("utf-8"))
        print("File transfer rejected.")

connection.close()
server.close()