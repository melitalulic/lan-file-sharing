import socket
import os

SERVER_IP = "ip_adresa"
SERVER_PORT = 8080

FILE_PATH = "file_path"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

filename = os.path.basename(FILE_PATH)
message = f"FILE_REQUEST:{filename}"
client.sendall(message.encode("utf-8"))

response = client.recv(1024)
response_message = response.decode('utf-8')
print(response_message)

if response_message.startswith("File sharing accepted:"):
    file_size = os.path.getsize(FILE_PATH)
    client.sendall(file_size.to_bytes(8, byteorder="big"))
    with open(FILE_PATH, "rb") as file:
        while True:
            data = file.read(65536)

            if not data:
                break

            client.sendall(data)

    print(f"File '{FILE_PATH}' successfully sent.")

client.close()