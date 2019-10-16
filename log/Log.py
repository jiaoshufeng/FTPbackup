import logging, os
from conf.setting import *


if LOGFILE:
    logpath = LOGFILEPATH
else:
    logpath = os.path.dirname(__file__)


def log_info(message, level='info'):
    level_list = {'info': logging.info,
                  'error': logging.error,
                  'warn': logging.WARN
                  }
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s, %(filename)s, %(levelname)s, %(message)s',

                        datefmt='%Y-%m-%d %H:%M:%S',

                        filename=os.path.join(logpath, 'log.txt'),

                        filemode='a')

    level_list[level](message)
