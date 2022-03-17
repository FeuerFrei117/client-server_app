'''
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать
скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря
в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
'''

import json
from pprint import pprint

'''
Подскажите, в моём решении файл надо закрывать?
И как проверить закрыт ли он?
'''


def write_order_to_json(item, quantity, price, buyer, date):
    info = {'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date}

    file = json.load(open('orders.json', encoding='utf-8'))
    file['orders'].append(info)
    json.dump(file, open('orders.json', 'w', encoding='utf-8'), indent=4)


write_order_to_json('Шаурма', 4, 200, 'Роман', '02.03.2022')
write_order_to_json('Чай', 6, 50, 'Илья', '02.03.2022')
write_order_to_json('Самса', 8, 150, 'Иван', '03.03.2022')

with open('orders.json', encoding='utf-8') as f_n:
    file = json.load(f_n)
    pprint(file)
