''' Программа-сервер '''
import logging
import select
import socket
import sys
import argparse
import time
import logs.server_log_config
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, \
    DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message
from decos import log

server_logger = logging.getLogger('server')

@log
def process_client_message(message, messages_list, client):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    отправляет словарь - ответ для клиента с результатом приема.

    :param message:
    :param message_list:
    :param client:
    :return:
    '''
    server_logger.debug(f'Разбор сообщения от клиента: {message}')
    # Если это сообщение о присутствии, принимаем и отвечаем, если успех
    if ACTION in message and\
            message[ACTION] == PRESENCE and\
            TIME in message and\
            USER in message and\
            message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and\
        message[ACTION] == MESSAGE and\
        TIME in message and\
        MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    # Иначе отдаем Bad request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def arg_parser():
    '''Парсер аргументов коммандной строки'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корректного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        server_logger.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    '''Загрузка параметров командной строки, если нет параметров, то задаем значения по умолчанию.'''
    listen_address, listen_port = arg_parser()

    server_logger.info(
        f'Запущен сервер, порт для подключений: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    # список клиентов, очередь сообщений
    clients = []
    messages = []

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    # Основной цикл программы сервера
    while True:
        # Ждем подключения, если таймаут вышел, ловим исключение.
        try:
            client, client_address = transport.accept()
        except OSError as err:
            print(err.errno)
            pass
        else:
            server_logger.info(f'Установлено соединение с ПК {client_address}')
            clients.append(client)

        recv_data_list = []
        send_data_list = []
        err_list = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_list, send_data_list, err_list = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладем в словарь, если ошибка, исключаем клиента.
        if recv_data_list:
            for client_with_message in recv_data_list:
                try:
                    process_client_message(get_message(client_with_message), messages, client_with_message)
                except:
                    server_logger.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиента, отправляем им сообщения.
        if messages and send_data_list:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_list:
                try:
                    send_message(waiting_client, message)
                except:
                    server_logger.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
