import socket
import threading


class Server:
    def __init__(self):
        self.ip = "localhost"
        self.port = 5555
        self.address = self.ip, self.port
        self.data = {
            "Players": {}
        }
        
    def handle_client(self, connection: socket.socket, id):
        connection.sendall(str(id[1]).encode())
        while True:
            player_data = connection.recv(1024).decode()
            self.data["Players"][id[1]] = eval(player_data)
            connection.sendall(str(self.data).encode())
        
        
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)
        self.server.listen(4)
        server_thread = threading.Thread(target=self._create_new_connections)
        server_thread.start()
            
    
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.address)
        return self.client
        
            
    def _create_new_connections(self):
        while True:
            connection, id = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(connection, id))
            thread.start()