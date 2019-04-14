from socket import AF_INET, socket, SOCK_DGRAM
from threading import Thread
import datetime
import time


def curr_time_send():
    while True:
        time.sleep(1.0)
        print(datetime.datetime.now())
        SERVER.sendto(bytes(str(datetime.datetime.now()), "utf8"), ADDR)


clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_DGRAM, 0)# семейство используемых протоколов
                                        # тип создаваемого сокета
                                        # TCP

if __name__ == "__main__":
    CURR_TIME = Thread(target=curr_time_send)
    CURR_TIME.start()
    CURR_TIME.join()
