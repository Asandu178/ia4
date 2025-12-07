# used for testing as of now
from board import *
from board.boardLogic import *
from gui.board_gui_pvp import boardDisplay as boardDisplayPvP
from gui.board_gui_pvb import boardDisplayPvB
# from gui.board_gui import boardDisplay
from game import chessGame
from game import human
from game import bot
from game import engine
from game import imageHandler
from network.network import Network
import server
import threading
from menu.central_menu import main_menu

def main():
    imageHandler.imageHandler.loadImages()
    engine.Engine.buildEngine()
    main_menu()

if __name__ == "__main__":
    main()


