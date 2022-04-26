'''
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Далее забыть о том, что мы сами только что создали этот файл и исходить из того, что перед нами файл в неизвестной
кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.
'''

import os
from chardet import detect

with open(os.getcwd() + '\\test_file.txt', 'rb') as f:
    content = f.read()
encod = detect(content)['encoding']
print(encod)

with open(os.getcwd() + '\\test_file.txt', 'r', encoding=encod) as f:
    print(f.read())
