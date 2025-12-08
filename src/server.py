import socket
import threading
import pickle

# Server class handles the network connection and game state synchronization
class Server:
    def __init__(self, host='0.0.0.0', port=5555, time_limit=None):
        # Create a TCP/IP socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reusing the address to avoid "Address already in use" errors on restart
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        # Bind the socket to the address and port
        self.server.bind((self.host, self.port))
        # Listen for incoming connections (max 2 players)
        self.server.listen(2)
        print("Waiting for a connection, Server Started")
        self.clients = []
        self.time_limit = time_limit

    # Broadcast data to all connected clients except the sender
    def broadcast(self, data, sender_conn):
        for client in self.clients:
            if client != sender_conn:
                try:
                    client.send(data)
                except:
                    # Remove client if sending fails
                    self.clients.remove(client)

    # Handle communication with a specific client
    def handle_client(self, conn, player_id):
        # Send initial configuration (player ID and time limit) to the client
        config = {
            'player_id': player_id,
            'time_limit': self.time_limit
        }
        conn.send(pickle.dumps(config))
        
        while True:
            try:
                # Receive data from the client
                data = conn.recv(2048)
                if not data:
                    print("Disconnected")
                    break
                
                # Broadcast the received data to other clients
                self.broadcast(data, conn)

            except:
                break

        print("Lost connection")
        try:
            self.clients.remove(conn)
            conn.close()
        except:
            pass

    # Main server loop to accept connections
    def run(self):
        current_player = 0
        self.running = True
        # Set a timeout to allow checking the running flag periodically
        self.server.settimeout(1.0) 
        while self.running:
            try:
                # Accept a new connection
                conn, addr = self.server.accept()
                print("Connected to:", addr)
                self.clients.append(conn)

                # Assign player ID: 0 for White, 1 for Black
                player_id = current_player
                current_player = (current_player + 1) % 2

                # Start a new thread to handle this client
                thread = threading.Thread(target=self.handle_client, args=(conn, player_id))
                thread.start()
            except socket.timeout:
                continue
            except OSError:
                # Socket closed, exit loop
                break
            except Exception as e:
                print(f"Server error: {e}")
                break

    # Stop the server and close all connections
    def stop(self):
        self.running = False
        try:
            self.server.close()
        except:
            pass
        # Close all client sockets
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients = []

if __name__ == "__main__":
    server = Server()
    server.run()
