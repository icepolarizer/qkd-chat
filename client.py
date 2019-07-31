from socket import *
import threading
import time
import sys
import alice, bob
# from simplecrypt import encrypt, decrypt, DecryptionException

key = "lemon-tea"
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


# AESCipher from: https://burningrizen.tistory.com/5
class AESCipher():

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def encrypt(self, raw):
        raw = self._pad(AESCipher.str_to_bytes(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')



def send(sock):
    while True:
        try:
            aes = AESCipher(key)
            sendData = aes.encrypt(input()).encode('utf-8')
            # sendData = encrypt(key, input())
            sock.send(sendData)
        except:
            continue


def receive(sock):
    while True:
        recvData = sock.recv(1024)
        try:
            aes = AESCipher(key)
            print('%s :'%opp_id, aes.decrypt(recvData))
            # print('%s :'%opp_id, decrypt(key, recvData).decode('utf-8'))
        except DecryptionException as e:
            print(e)


port = int(sys.argv[1])

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('localhost', port))

user_id = str(input("ID: "))
clientSock.send(user_id.encode('utf-8'))

# user_list = clientSock.recv(1024).decode('utf-8')
# print("USER LIST: {}".format(user_list))

opp_id = str(input("Enter the opponent's id: "))

if opp_id:
    print(key)
    clientSock.send(opp_id.encode('utf-8'))

    print("Tunnel established. Strting Quantum Key Distribution...")
    key = str(alice.key())
    time.sleep(1)
    print("Polarity Filter Array,  A.K.A ALICE Key has generated. Starting Qubit transfer phase.")
    time.sleep(1)
    print("Sending Qubits and Circuits to Server, Pickled...")
    time.sleep(1)
    with open('alice.laser', 'rb') as file:
        clientSock.send(file.read())
else:
    clientSock.send("~".encode('utf-8'))
    print("Opponent's id is blank. Wating for connection request...")
    opp_id = clientSock.recv(1024).decode('utf-8')
    print("Request from <%s>. Accepting."%opp_id)
    time.sleep(1)
    print("Recieveing Qubits/Filter/Circuits from <%s>..."%opp_id)
    time.sleep(1)
    laser = clientSock.recv(2048)
    with open('bob.laser', 'wb') as file:
        file.write(laser)
    key = str(bob.key())


print("LINK START!")
print("Final AES Encryption Key: ", key)


sender = threading.Thread(target=send, args=(clientSock,))
receiver = threading.Thread(target=receive, args=(clientSock,))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass