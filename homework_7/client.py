''' Программа-клиент '''
import logging
import sys
import json
import socket
import time
import argparse
import logs.client_log_config
from errors import ReqFieldMissingError, ServerError
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT, MESSAGE, SENDER, MESSAGE_TEXT
from common.utils import get_message, send_message
from decos import log

client_logger = logging.getLogger('client')

@log
def message_from_server(message):
    # Функция - обработчик соощений других пользователей, поступающих с сервера
    if ACTION in message and\
        message[ACTION] == MESSAGE and\
        SENDER in message and\
        MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        client_logger.info(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        client_logger.error(f'Получено некорректное сообщение с сервера: {message}')

@log
def create_message(sock, account_name='Guest'):
    '''
    Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной команды.
    '''
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        client_logger.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    client_logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict

@log
def create_presence(account_name='Guest'):
    '''Функция генерирует запрос о присутствии клиента'''
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    client_logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def process_response_ans(message):
    '''
    Функция разбирает ответ сервера на сообщение о присутствии,
    возвращает 200 если все ОК или генерирует исключение при ошибке
    '''
    client_logger.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@log
def arg_parser():
    '''
    Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    # Проверим подходящий номер порта
    if not 1023 < server_port < 65536 :
        client_logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        client_logger.critical(f'Указан недопустимый режим работы {client_mode}, '
                               f'допустимые режимы: listen, send')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    ''' Загружаем параметры коммандной строки '''
    server_address, server_port, client_mode = arg_parser()

    client_logger.info(f'Запущен клиент с параметрами: адрес сервера: {server_address}, '
                       f'порт: {server_port}, режим работы: {client_mode}')

    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_response_ans(get_message(transport))
        client_logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        client_logger.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        client_logger.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        client_logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        client_logger.critical(f'Не удалось подключиться к серверу {server_address}:{server_port},'
                               f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл программы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - прием сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

            # Режим работы прием:
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
