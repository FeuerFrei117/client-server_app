'''
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из
файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в
него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
'''
import csv
import os
import re
from pprint import pprint

from chardet import detect

files = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы'],
                 os_prod_list, os_name_list, os_code_list, os_type_list]

    for file in files:
        with open(os.path.join(os.getcwd(), file), 'rb') as f:
            content = f.read()
        encod = detect(content)['encoding']

        with open(os.path.join(os.getcwd(), file), 'r', encoding=encod) as f:
            for line in f:
                result = re.split(r':', line)
                if 'Изготовитель системы' in result:
                    os_prod_list.append(result[1].strip())
                if 'Название ОС' in result:
                    os_name_list.append(result[1].strip())
                if 'Код продукта' in result:
                    os_code_list.append(result[1].strip())
                if 'Тип системы' in result:
                    os_type_list.append(result[1].strip())

    return main_data


def write_to_csv(link):
    data = get_data()
    new_data = [data[0]]
    for i in range(len(data[1])):
        result = []
        for t in range(1, len(data)):
            result.append(data[t][i])
        new_data.append(result)

    with open(link, 'w', encoding='utf-8') as f:
        data = csv.writer(f)
        data.writerows(new_data)


write_to_csv(os.path.join(os.getcwd(), 'file_for_ex_1.csv'))

'''
Не понимаю почему вывод идет с дополнительно вставленными пустыми списками.
Это нормально или это особенность записи в csv?
'''

with open('file_for_ex_1.csv', encoding='utf-8') as f:
    date = csv.reader(f)
    pprint(list(date))
