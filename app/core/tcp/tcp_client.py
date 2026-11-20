import socket

SERVER_IP = "ip_adresa"
SERVER_PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((SERVER_IP, SERVER_PORT))

message = "FILE_REQUEST:slika.jpg"
client.sendall(message.encode("utf-8"))

response = client.recv(1024)
response_message = response.decode('utf-8')

print(response_message)

client.close()