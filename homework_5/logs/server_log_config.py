import logging
import os
import sys
from logging import handlers
from common.variables import LOGGING_LEVEL
sys.path.append('../')

server_formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(module)-8s - %(message)s ')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server_log_config.log')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(server_formatter)
stream_handler.setLevel(logging.DEBUG)
log_file = handlers.TimedRotatingFileHandler(PATH, when='D', interval=1, encoding='utf-8')
log_file.setFormatter(server_formatter)

logger = logging.getLogger('server')
logger.addHandler(stream_handler)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')
    logger.warning('Предупреждение')
    logger.error('Ошибка')
    logger.critical('Критическое сообщение')
