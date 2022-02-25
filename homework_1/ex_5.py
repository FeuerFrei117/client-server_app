'''
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на
кириллице.
'''
import chardet
import platform
import subprocess

sites = ['yandex.ru', 'youtube.com']

param = '-n' if platform.system().lower() == 'windows' else '-c'
for site in sites:
    args = ['ping', param, '4', site]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in process.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding'])
        print(line)
    print('*' * 70)
