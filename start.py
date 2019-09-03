class BracketError(Exception):
    pass


# Функция проверки скобок
def bracket_analysis(e):
    level = 0
    for c in e:
        if c == '(':
            level += 1
        if c == ')':
            level -= 1
        if level < 0:
            raise BracketError
    if level != 0:
        raise BracketError


# Начало выполнения программы
while True:
    expr = input('Введите выражение: ')
    expr = expr.lower().replace(' ', '')
    if expr == 'quit' or expr == 'q' or expr == 'exit' or expr == 'x':
        break
    expr = '(' + expr + ')'
    try:
        bracket_analysis(expr)
    except BracketError:
        print('Не удалось вычислить значение выражения')
