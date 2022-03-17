'''
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое и
выполнить обратное преобразование (используя методы encode и decode).
'''

words = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words:
    new_word = word.encode('utf-8')
    print(new_word)
    print(new_word.decode('utf-8'))
    print('')
