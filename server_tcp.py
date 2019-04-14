from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import base64
import datetime
import re
import time


def accept_incoming_connections():
    """Присоединение клиента но стороне клиента."""
    while True:
        """извлечение запросов на соединение из очереди"""
        client, client_address = SERVER.accept() # порт и IP
        #print("%s:%s присоединился." % client_address)
        client.send(bytes("Соединение установлено. Введите свое имя:", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def file_work(client):
    client.send(bytes("Введите имя файла, смещение и размер блока через пробел.", "utf-8"))
    file_info_str = client.recv(BUFSIZ).decode("utf-8")
    file_info_list = file_info_str.split()
    file_path = file_info_list[0]
    file_offset = file_info_list[1]
    file_block_size = file_info_list[2]
    file = open(file_path, "rb")
    file.seek(int(file_offset))
    data = file.read(int(file_block_size))
    file.close()
    new_file = open("newFile.txt", "wb")
    new_file.write(data)
    new_file.close()
    client.send(base64.b64encode(data))


def text_work(client):
    client.send(bytes("Введите текст:", "utf-8"))
    text = client.recv(BUFSIZ).decode("utf-8")
    words = filter(None, re.split("[ ,!?:;]+", text))
    client.send(bytes(str(len(list(words))), "utf-8"))


def handle_client(client):  # Takes client socket as argument.
    """Присоединение клиента."""
    name = client.recv(BUFSIZ).decode("utf-8")
    clients[client] = name

    while True:
        client.send(bytes("1 - работа с файлом, 2 - работа с текстом, 3 - выход", "utf-8"))
        client_choise = client.recv(BUFSIZ).decode("utf-8")
        if client_choise == "1":
            file_work(client)
        elif client_choise == "2":
            text_work(client)
        elif client_choise == "3":
            client.close()
            del clients[client]
            break
        else:
            client.send(bytes("Ошибка", "utf-8"))


def curr_time_send():
    while True:
        time.sleep(5.0)
        print(datetime.datetime.now())
        for sock in clients:
            sock.send(bytes(str(datetime.datetime.now()), "utf8"))



clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM, 0)# семейство используемых протоколов
                                        # тип создаваемого сокета
                                        # TCP
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    #ACCEPT_THREAD.join()
    CURR_TIME = Thread(target=curr_time_send)
    CURR_TIME.start()
    #CURR_TIME.join()
    ACCEPT_THREAD.join()
    #SERVER.close()