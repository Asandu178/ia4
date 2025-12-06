# used for testing as of now
from board import *
from board.boardLogic import *
from gui.board_gui_pvp import boardDisplay as boardDisplayPvP
from gui.board_gui_pvb import boardDisplayPvB
from gui.board_gui import boardDisplay
from game import chessGame
from game import human
from game import bot
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
         boardDisplayPvP()
    elif choice == '2':
        # Start server
        s = server.Server()
        t = threading.Thread(target=s.run)
        t.daemon = True
        t.start()
        
        network = Network()
        player_color = 'white'
        boardDisplayPvP(network=network, player_color=player_color)
        
    elif choice == '3':
        ip = input("Enter Host IP (default localhost): ") or 'localhost'
        network = Network(ip)
        player_color = 'black'
        boardDisplayPvP(network=network, player_color=player_color)

    elif choice == '4':
        # Player1 = human.Human('white', 'Marius', 600)
        # Player2 = bot.Bot('black', 'Andrei', 600)
        boardDisplayPvB()

if __name__ == "__main__":
    main()


