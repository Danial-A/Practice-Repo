import socket
import threading
from queue import Queue

NUMBER_OF_THREAD = 2
JOBS = [1, 2]

queue = Queue()

s = socket.socket()
host = '127.0.0.1'    #write host server IP
port = 5000

s.connect((host, port))


def send_message():
    while True:
        try:
            #print("Yeah im coming here")
            message = input("Client: ")
            s.send(str.encode(message, 'utf-8'))
        except:
            print("error in sending ")
            break


def recv_message():
    while True:
        try:
            message = str(s.recv(20480), 'utf-8')
            print("\n" + message)
        except:
            print("error in receiving")
            break


def create_workers():
    for _ in range(NUMBER_OF_THREAD):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()

        if x == 1:
            send_message()
        if x == 2:
            recv_message()

        queue.task_done()


def create_jobs():
    for x in JOBS:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()