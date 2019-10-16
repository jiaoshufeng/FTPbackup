from os import path
from sys import path as sys_path
import time


sys_path.insert(0, path.dirname(path.dirname(__file__)))

from core.Main import start
from log.Log import log_info
if __name__ == '__main__':
    start()
    time.sleep(2)