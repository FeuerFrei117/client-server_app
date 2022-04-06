"""
Написать программу, которая будет складывать, вычитать, умножать или делить два числа. Числа и знак операции вводятся
пользователем. После выполнения вычисления программа не должна завершаться, а должна запрашивать новые данные для
вычислений. Завершение программы должно выполняться при вводе символа '0' в качестве знака операции. Если пользователь
вводит неверный знак (не '0', '+', '-', '*', '/'), то программа должна сообщать ему об ошибке и снова запрашивать знак
операции. Также сообщать пользователю о невозможности деления на ноль, если он ввел 0 в качестве делителя.
"""


def my_fun(number_one, number_two, operations):

    if isinstance(number_one, int) and isinstance(number_two, int) and operations in ['+', '-', '*', '/']:
        if operations == '+':
            return number_one + number_two
        if operations == '-':
            return number_one + number_two
        if operations == '*':
            return number_one * number_two
        if operations == '/':
            if number_two == 0:
                return 'Делить на "0" нельзя!'
            else:
                return number_one / number_two
    else:
        return 'TypeError'


if __name__ == '__main__':
    while True:
        action = ["+", "-", "*", "/"]
        try:
            num_one = int(input('Введите первое число: '))
            num_two = int(input('Введите второе число: '))
            operat = input(f'Введите необходимое действие ({action}), для выхода введите "0": ')

            if operat == '0':
                print('До скорой встречи')
                break

            print(my_fun(num_one, num_two, operat))

        except ValueError:
            print('Вы ввели не число')
            continue
