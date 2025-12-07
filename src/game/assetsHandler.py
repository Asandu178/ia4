import os
import time
from subprocess import Popen, PIPE, STDOUT
class assetsHandler:
    def __init__(self):
        pass

    @staticmethod
    def loadAssets(pathToAssets="./assets"):
        if not os.path.exists(pathToAssets):
            p = Popen(["wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1p-JwTAiwdC0S25hBhbKXANm8Zpt7vJCk' -O assets.zip"], shell=True)
            time.sleep(10)
            p = Popen(["unzip assets.zip"], shell=True)
            time.sleep(5)
            p = Popen(["rm assets.zip"], shell=True)