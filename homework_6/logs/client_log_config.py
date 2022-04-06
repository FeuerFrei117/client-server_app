import logging
import os
import sys
from common.variables import LOGGING_LEVEL
sys.path.append('../')

client_formatter = logging.Formatter("%(asctime)s %(levelname)s - %(module)s - %(message)s")

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(client_formatter)
stream_handler.setLevel(logging.DEBUG)

log_file = logging.FileHandler(PATH, encoding='utf-8')
log_file.setFormatter(client_formatter)

logger = logging.getLogger('client')
logger.addHandler(stream_handler)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)


if __name__ == '__main__':
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')
    logger.warning('Предупреждение')
    logger.error('Ошибка')
    logger.critical('Критическое сообщение')














