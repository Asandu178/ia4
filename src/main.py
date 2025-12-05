# used for testing as of now
from board import *
from board.boardLogic import *
from gui.board_gui_pvp import boardDisplay
from gui.board_gui_pvb import boardDisplayPvB
from game import chessGame
from network.network import Network
import server
import threading

def main():
    print("1. Local Play (PvP)")
    print("2. Host Game")
    print("3. Join Game")
    print("4. Player vs Bot")
    choice = input("Enter choice: ")

    network = None
    player_color = None

    if choice == '1':
         boardDisplay()
    elif choice == '2':
        # Start server
        s = server.Server()
        t = threading.Thread(target=s.run)
        t.daemon = True
        t.start()
        
        network = Network()
        player_color = 'white'
        boardDisplay(network=network, player_color=player_color)
        
    elif choice == '3':
        ip = input("Enter Host IP (default localhost): ") or 'localhost'
        network = Network(ip)
        player_color = 'black'
        boardDisplay(network=network, player_color=player_color)

    elif choice == '4':
        boardDisplayPvB()

if __name__ == "__main__":
    main()


