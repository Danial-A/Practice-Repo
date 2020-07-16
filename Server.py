import socket
import threading
from queue import Queue

NUMBER_OF_THREAD = 3
JOBS = [1, 2, 3]

all_conn = []
all_addr = []

queue = Queue()

conn1 = None


def create_socket():
    try:
        global host
        global port
        global s

        s = socket.socket()
        host = ''
        port = 5000

        print("Socket Created")
    except socket.error as msg:
        print("error creating the socket " + str(msg))


def bind_socket():
    global host
    global port
    global s

    print("Socket binded to : " + str(port))
    s.bind((host, port))
    s.listen(5)
    print("Socket is Listening")


def accept_connections():
    for c in all_conn:
        c.close()

    del all_addr[:]
    del all_conn[:]

    while True:
        try:
            conn, addr = s.accept()
            s.setblocking(1)

            all_conn.append(conn)
            all_addr.append(addr)

            print("Connections accepted from : " + addr[0])
        except:
            print("error in accepting connections")


def start_terminal():
    while True:
        message = input("turtle> ")
        if message == 'list':
            list_connections()
        elif 'select' in message:
            conn = get_target(message)
            if conn is not None:
                send_message(conn)
        else:
            print("command not recognized")


def list_connections():
    print("----Clients----- \n ")
    for i, conn in enumerate(all_conn):
        try:
            conn.send(str.encode(' '))
            # conn.recv(201480)
        except:
            del all_addr[i]
            del all_addr[i]
            continue

        print(str(i) + "   " + str(all_addr[i][0]) + "    " + str(all_addr[i][1]))


def get_target(message):
    global conn1
    try:
        target = message.replace('select ', '')
        target = int(target)

        conn1 = all_conn[target]
        print("You are now connected to : " + str(all_addr[target][0]))
        print( str(all_addr[target][0]) + "> ", end='')
        return conn1
    except:
        print("selection no valid")
        return None


def send_message(conn):
    while True:
        try:
            msg = input("Server Message: ")
            if msg == 'quit':
                break;
            if len(str.encode(msg)) > 0:
                conn.send(str.encode(msg))
                # client_resp = str(conn.recv(20480,'utf-8'))
                # print(client_resp, end='')
        except:
            print("error sending message")
            break


def recv_message():
    # print("recv message")
    global conn1
    while True:
        try:
            if conn1 is not None:
                msg = str(conn1.recv(20480), 'utf-8')
                print("Client Message: " + msg)
        except:
            print("error in recieving messages from client")
            break
    for n in all_conn:
        conn.send(msg.encode('utf-8'))


def create_workers():
    for _ in range(NUMBER_OF_THREAD):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()

        if x == 1:
            create_socket()
            bind_socket()
            accept_connections()
        if x == 2:
            start_terminal()
        if x == 3:
            recv_message()

        queue.task_done()


def create_jobs():
    for x in JOBS:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()