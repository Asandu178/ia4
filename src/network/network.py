import socket
import pickle
import select

# Network class to handle client-side connection to the server
class Network:
    def __init__(self, server_ip='localhost'):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_ip
        self.port = 5555
        self.addr = (self.server, self.port)
        # Connect and retrieve initial player configuration
        self.player_id = self.connect()

    # Establish connection to the server and receive initial settings (ID, time limit)
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

    # Send data to the server
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)

    # Receive data from the server with a non-blocking check
    def receive(self):
        try:
            # Check if there is data to be read
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
