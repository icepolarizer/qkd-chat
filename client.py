from socket import *
import threading
import time
import sys
import alice, bob
from simplecrypt import encrypt, decrypt, DecryptionException

key = "lemon-tea"

def send(sock):
    while True:
        sendData = encrypt(key, input())
        sock.send(sendData)


def receive(sock):
    while True:
        recvData = sock.recv(1024)
        try:
            print('%s :'%opp_id, decrypt(key, recvData).decode('utf-8'))
        except DecryptionException:
            pass


port = int(sys.argv[1])

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', port))

user_id = str(input("ID: "))
clientSock.send(user_id.encode('utf-8'))

# user_list = clientSock.recv(1024).decode('utf-8')
# print("USER LIST: {}".format(user_list))

opp_id = str(input("연결 대상자의 ID를 입력하십시오: "))

if opp_id:
    print(key)
    clientSock.send(opp_id.encode('utf-8'))

    key = str(alice.key())
    with open('laser.alice', 'rb') as file:
        clientSock.send(file.read())
else:
    clientSock.send("~".encode('utf-8'))
    print("교신 대상 ID 공백. 교신 대기.")
    opp_id = clientSock.recv(1024).decode('utf-8')
    print(opp_id)
    laser = clientSock.recv(2048)
    with open('laser.bob', 'wb') as file:
        file.write(laser)
    key = str(bob.key())

print("KEEEEYYYYYEYYEYYYY: ", key)


sender = threading.Thread(target=send, args=(clientSock,))
receiver = threading.Thread(target=receive, args=(clientSock,))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass