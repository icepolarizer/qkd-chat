from socket import *
import threading
import time
import sys
import logging


clients = {}


def send(sock, data):
    try:
        sock.send(data.encode('utf-8'))
    except error as e:
        logging.error(e)


def comm(sock1, sock2): # Relay message from sock1 to sock2
    while True:
        data = sock1.recv(2048)
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
            print('Request from ', str(addr), 'connection successful.')

            user_id = sock.recv(2048).decode('utf-8')
            clients[user_id] = sock

            print("Link request from %s." % user_id)

            # send(sock, str(list(clients.keys())))

            try:
                print("Waiting for Opponent's ID...")
                opp_id = sock.recv(2048).decode('utf-8')
                print("ID Recieved.")
            except UnicodeDecodeError:
                print("Invalid ID")
                # send(sock, "No valid ID")
                continue

            if opp_id == "~":
                print("Blank id. Corresponding user will go into sleep mode")
                continue


            if opp_id not in clients:
                print("No such user")
                # send(sock, "Can't find user")
                continue

            print("Receiving LASER...")
            laser = sock.recv(2048) # Recieve Pickled Qubits


            send(clients[opp_id], user_id)

            print("Link request from %s to %s. Linking..."%(user_id, opp_id))

            clients[opp_id].send(laser)

            threading.Thread(target=comm, args=(clients[user_id], clients[opp_id])).start()
            threading.Thread(target=comm, args=(clients[opp_id], clients[user_id])).start()

            print(clients)

        except error as e:
            logging.error(e)


port = int(sys.argv[1])

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)

print('PORT %d, waiting fror request...'%port)

connector = threading.Thread(target=connect)
connector.start()

while True:
    time.sleep(1)
    pass