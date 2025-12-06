import socket
import pickle
import select

class Network:
    def __init__(self, server_ip='localhost'):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_ip
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            # Receive pickle data directly
            data = self.client.recv(2048)
            config = pickle.loads(data)
            self.time_limit = config.get('time_limit')
            return config.get('player_id')
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            ready = select.select([self.client], [], [], 0.01)
            if ready[0]:
                data = self.client.recv(4096)
                if not data:
                    return None
                return pickle.loads(data)
            return None
        except socket.error as e:
            print(e)
            return None
