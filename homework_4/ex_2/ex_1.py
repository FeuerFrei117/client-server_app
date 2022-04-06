# Программа принимает действительное положительное число x и целое отрицательное число y. Необходимо выполнить
# возведение числа x в степень y. Задание необходимо реализовать в виде функции my_func(x, y). При решении задания
# необходимо обойтись без встроенной функции возведения числа в степень.
#
# Подсказка: попробуйте решить задачу двумя способами. Первый — возведение в степень с помощью оператора **.
# Второй — более сложная реализация без оператора **, предусматривающая использование цикла.


def my_func(x, y):
    if isinstance(x, int) and isinstance(y, int):
        i = 0
        x_to_the_y_power = 1
        while i != abs(y):
            x_to_the_y_power = x * x_to_the_y_power
            i += 1
        x_to_the_minus_y = 1 / x_to_the_y_power
        return x_to_the_minus_y
    else:
        return 'TypeError'


if __name__ == '__main__':

    input_user_number_one = int(input('Введите действительное положительное число: '))
    input_user_number_two = int(input('Введите целое отрицательное число: '))

    print(my_func(input_user_number_one, input_user_number_two))
