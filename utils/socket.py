import socket
import threading

import asyncio

class Server:
    def __init__(self, host):
        self.host = host
        self.port = 5000
        self.clients = []

    async def handle_client(self, client_reader, client_writer):
        self.clients.append(client_writer)
        addr = client_writer.get_extra_info('peername')
        print("Connected to", addr)

        while True:
            try:
                data = await client_reader.read(1024)
                if not data:
                    break
                self.broadcast(data.decode(), client_writer)
            except ConnectionResetError:
                self.clients.remove(client_writer)
                break

        client_writer.close()
        print("Disconnected from", addr)

    def broadcast(self, data, sender_writer):
        for client_writer in self.clients:
            if client_writer != sender_writer:
                client_writer.write(data.encode())

    async def start(self):
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )

        addr = server.sockets[0].getsockname()
        print("Server started. Listening on", addr)

        async with server:
            await server.serve_forever()

    def stop(self):
        for client_writer in self.clients:
            client_writer.close()
        print("Server closed.")

class Client:
    def __init__(self):
        self.host = None
        self.port = 5000
        self.client_socket = None
    
    def setHost(self, host):
        self.host = host

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print("Connected to server.")

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def receive(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                print("Received:", data)
            except ConnectionResetError:
                print("Disconnected from server.")
                break

    def send(self, data):
        self.client_socket.sendall(data.encode())

    def disconnect(self):
        self.client_socket.close()
        print("Disconnected from server.")