import socket
import threading
import pickle

class Server:
    def __init__(self, host='0.0.0.0', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.server.bind((self.host, self.port))
        self.server.listen(2)
        print("Waiting for a connection, Server Started")
        self.clients = []

    def broadcast(self, data, sender_conn):
        for client in self.clients:
            if client != sender_conn:
                try:
                    client.send(data)
                except:
                    self.clients.remove(client)

    def handle_client(self, conn, player_id):
        conn.send(str.encode(str(player_id)))
        while True:
            try:
                data = conn.recv(2048)
                if not data:
                    print("Disconnected")
                    break
                
                self.broadcast(data, conn)

            except:
                break

        print("Lost connection")
        try:
            self.clients.remove(conn)
            conn.close()
        except:
            pass

    def run(self):
        current_player = 0
        while True:
            conn, addr = self.server.accept()
            print("Connected to:", addr)
            self.clients.append(conn)

            # Assign player 0 (White) or 1 (Black)
            # Simple logic: first to connect is White
            player_id = current_player
            current_player = (current_player + 1) % 2

            thread = threading.Thread(target=self.handle_client, args=(conn, player_id))
            thread.start()

if __name__ == "__main__":
    server = Server()
    server.run()
