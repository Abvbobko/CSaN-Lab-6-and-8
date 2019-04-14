from socket import AF_INET, socket, SOCK_DGRAM

HOST = "127.0.0.1"
PORT = 33000

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_DGRAM, 0) # AF_INET - семейство протоколов для интернет соединений
# тип сокета
client_socket.bind(ADDR)# сервер

while True:
    data = client_socket.recvfrom(1024)[0]
    data = data.decode()
    print(str(data))
