import socket
import threading
import time

class Server():
    def __init__(self):
        #SERVER
        host = '192.168.137.1'
        port = 5555
        self.locaddr = (host, port)

        #CLIENT
        self.M_SIZE = 1024

        #VARIABLE
        self.clients = []

        #FUNC
        threading.Thread(target=lambda: self.send(),args=()).start()
        self.socket_create()

    def send(self):
        while True:
            command = input("c> ")
            if command != "":
                for client in self.clients:
                    client.send((command+"!").encode('ascii'))

    def socket_create(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.locaddr)
            self.server.listen()
            self.receive()
        except Exception as err: print(err)

    def receive(self):
        while True:
            try:
                client, address = self.server.accept()
                print(f"Connected with {str(address)}")
                self.clients.append(client)
                threading.Thread(target=lambda: self.handle(client,address),args=()).start()
            except Exception as err: print(err)
            
    def handle(self,client,addr):
        while True:
            try:
                message = client.recvfrom(self.M_SIZE)
                msg = message[0].decode(encoding='utf-8')
                if msg =="c0": #接続確認
                    client.send("s0!".encode('ascii'))
                if msg =="c1": #接続終了
                    print(str(addr)+"connection is finished")
                    self.clients.remove(client)
                    break
            except Exception as err: 
                print(err)
                break

Server()