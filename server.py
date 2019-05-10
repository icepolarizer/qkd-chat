from socket import *
import threading
import time
import sys


clients = {}


def send(sock, data):
    try:
        sock.send(data.encode('utf-8'))
    except error as e:
        print(e)


def comm(sock1, sock2): # Relay message from sock1 to sock2
    while True:
        data = sock1.recv(1024)
        print(data)
        if data:
            sock2.send(data)
        else:
            break


def connect():
    # 여기에 QKD 삽입
    while True:
        try:
            sock, addr = serverSock.accept()
            # user_id = int(time.time())
            print(str(addr), '에서 접속 요청을 확인. 접속에 성공하였습니다.')

            user_id = sock.recv(1024).decode('utf-8')
            clients[user_id] = sock

            print("%s에서 링크 요청." % user_id)

            # send(sock, str(list(clients.keys())))

            try:
                print("링크 대상 ID 수신 대기...")
                opp_id = sock.recv(1024).decode('utf-8')
                print("링크 대상 ID 수신함.")
            except UnicodeDecodeError:
                print("ID에 결함.")
                # send(sock, "No valid ID")
                continue

            if opp_id == "~":
                print("교신 대상 ID 공백. 해당 유저는 교신 대기 상태로 전환.")
                continue


            if opp_id not in clients:
                print("해당 유저 존재하지 않음.")
                # send(sock, "Can't find user")
                continue

            print("Receiving LASER...")
            laser = sock.recv(2048) # Recieve Pickled Qubits


            send(clients[opp_id], user_id)

            print("%s에서 %s로의 링크 요청을 확인. 링크합니다."%(user_id, opp_id))

            clients[opp_id].send(laser)

            threading.Thread(target=comm, args=(clients[user_id], clients[opp_id])).start()
            threading.Thread(target=comm, args=(clients[opp_id], clients[user_id])).start()

            print(clients)

        except error as e:
            print(e)


port = int(sys.argv[1])

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)

print('%d번 포트, INCOM 접속 대기중...'%port)

connector = threading.Thread(target=connect)
connector.start()

while True:
    time.sleep(1)
    pass