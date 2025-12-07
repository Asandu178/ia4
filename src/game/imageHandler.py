import os
import time
from subprocess import Popen, PIPE, STDOUT
class imageHandler:
    def __init__(self):
        pass

    @staticmethod
    def loadImages(pathToAssets="./assets"):
        if not os.path.exists(pathToAssets):
            p = Popen(["unzip assets.zip"], shell=True)
            time.sleep(5)