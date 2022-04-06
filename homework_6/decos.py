
import sys
import logging
import logs.client_log_config
import logs.client_log_config
import traceback
import inspect

def log(func_to_log):
    def log_saver(*args, **kwargs):
        logger_name = 'server' if 'server.py' in sys.argv[0] else 'client'
        LOGGER = logging.getLogger(logger_name)

        ret = func_to_log(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} с параметрами {args}, {kwargs}.'
                     f'Вызов из модуля {func_to_log.__module__}.'
                     f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     
                     f'Вызов из функции {inspect.stack()[1][3]}'
                     
                     f'@@@Вызов из функции {sys._getframe().f_back.f_code.co_name}'
                     f'@@@Вызов из модуля {sys._getframe().f_back.f_code.co_filename.split("/")[-1]}')
        return ret
    return log_saver
