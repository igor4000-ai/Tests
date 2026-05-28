
def discriminant(a, b, c):
    """
    функция для нахождения дискриминанта
    """
    # Ваш алгоритм
    d = b ** 2 - 4 * a * c
    if d < 0:
        return 'корней нет'
    elif d == 0:
        x1 = -b / (2 * a)
        return x1
    else:
        x1 = (-b + d ** 0.5) / (2 * a)
        x2 = (-b - d ** 0.5) / (2 * a)
        return x1, x2

def solution(a, b, c):
    """
    функция для нахождения корней уравнения
    """
    d = b ** 2 - 4 * a * c
    if d < 0:
        print('корней нет')
    elif d == 0:
        x1 = -b / (2 * a)
        return x1
    else:
        x1 = (-b + d ** 0.5) / (2 * a)
        x2 = (-b - d ** 0.5) / (2 * a)
        return  x1, x2