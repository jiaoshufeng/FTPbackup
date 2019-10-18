from os import path
from sys import path as sys_path


sys_path.insert(0, path.dirname(path.dirname(__file__)))

from core.Main import start
if __name__ == '__main__':
    start()