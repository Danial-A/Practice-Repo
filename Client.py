import socket

s = socket.socket()

port = 5000

s.connect(('127.0.0.1', port))

message=''
while message!='Over':
    #message = input("Client: ")
    s.send(message.encode())
    print(s.recv(1024))

s.close()