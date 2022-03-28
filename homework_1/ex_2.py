'''
Каждое из слов «class», «function», «method» записать в байтовом типе. Сделать это необходимо в автоматическом, а не
ручном режиме, с помощью добавления литеры b к текстовому значению, (т.е. ни в коем случае не используя методы encode,
decode или функцию bytes) и определить тип, содержимое и длину соответствующих переменных.
'''

words = ['class', 'function', 'method']
words_byte = []

for word in words:
    words_byte.append(eval(f'b"{word}"'))

for word in words_byte:
    print(f'Содержимое: {word}, Тип: {type(word)}, Длина: {len(word)}')
