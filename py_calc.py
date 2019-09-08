import math

# Типы элементов выражения
OPEN_BRACKET = ['(']
CLOSE_BRACKET = [')']
OPERATIONS = list('+-*/^')
NUMBERS = list('0123456789.')
SYMBOLS = [chr(a) for a in range(ord('a'), ord('z') + 1)]

# Константы
CONSTANTS = {'pi': math.pi, 'e': math.e}

# Стандартные математические функции
FUNCTIONS = {'sin': math.sin,
             'cos': math.cos,
             'tan': math.tan,
             'cotan': (lambda x: 1 / math.tan(x)),
             'abs': math.fabs,
             'ln': math.log,
             'log': math.log2,
             'lg': math.log10,
             'sqrt': math.sqrt,
             'exp': math.exp}


# Класс для представления отдельных элементов выражения
class Element:

    def __init__(self, type_of_content, content):
        self.type_of_content = type_of_content
        self.content = content

    def get_float_content(self):
        return float(self.content)

    def append_to_content(self, a):
        self.content += a


# Функция проверки правильности расстановки скобок
def bracket_analysis(expr):
    level = 0
    for c in expr:
        if c == '(':
            level += 1
        if c == ')':
            level -= 1
        if level < 0:
            raise Exception
    if level != 0:
        raise Exception


# Функция, разбивающая выражение на отдельные элементы
def parser(expr):
    result = []
    for char in expr:
        if char in OPEN_BRACKET:
            result.append(Element('open_bracket', char))
            continue
        if char in CLOSE_BRACKET:
            result.append(Element('close_bracket', char))
            continue
        if char in OPERATIONS:
            result.append(Element('operation', char))
            continue
        if char in NUMBERS:
            if len(result) == 0:
                result.append(Element('number', char))
                continue
            if result[-1].type_of_content == 'number':
                result[-1].append_to_content(char)
                continue
            result.append(Element('number', char))
            continue
        if char in SYMBOLS:
            if len(result) == 0:
                result.append(Element('symbol', char))
                continue
            if result[-1].type_of_content == 'symbol':
                result[-1].append_to_content(char)
                continue
            result.append(Element('symbol', char))
            continue
        raise Exception
    return result


# Функция, вычисляющая значение выражения
def calculate(expr):
    # Анализируем правильность расстановки скобок
    expr = '(' + expr + ')'
    bracket_analysis(expr)

    # Парсим выражение на отдельные элементы: числа, скобки, знаки операций и т.д.
    expr = parser(expr)

    # В цикле итеративно вычисляем значение выражения
    # Для этого последовательно разбиваем его на подвыражения, построенные только из чисел и операций +, -, *, /, ^
    while True:

        # Ищем подходящее для вычисления подвыражение, заключенное в скобки
        pos_start = 0
        pos_end = 0
        pos = 0
        for p in expr:
            if p.type_of_content == 'open_bracket':
                pos_start = pos
            if p.type_of_content == 'close_bracket':
                pos_end = pos
                break
            pos += 1
        sub_expr = expr[pos_start + 1: pos_end]

        # Первый этап вычисления значения подвыражения - разрешение всех функций и констант в нем в числа
        resolved_sub_expr = []
        skip_flag = False
        for i in range(len(sub_expr)):
            if skip_flag:
                skip_flag = False
                continue
            p = sub_expr[i]
            if p.type_of_content == 'symbol':
                if p.content in CONSTANTS.keys():
                    resolved_sub_expr.append(Element('number', CONSTANTS[p.content]))
                    continue
                if p.content in FUNCTIONS.keys():
                    resolved_sub_expr.append(
                        Element('number', FUNCTIONS[p.content](sub_expr[i + 1].get_float_content())))
                    skip_flag = True
                    continue
                raise Exception
            resolved_sub_expr.append(p)
        sub_expr = resolved_sub_expr

        # Второй этап вычисления подвыражения - удаление унарного минуса (при наличии) в начале выражения
        if sub_expr[0].content == '-':
            sub_expr[1].content = sub_expr[1].get_float_content() * (-1)
            del sub_expr[0]

        # Третий этап вычисления подвыражения - итеративное вычисление результатов элементарных операций +, -, /, *, ^
        while True:
            # Если подвыражение содержит одно значение, то его можно считать вычисленным
            if len(sub_expr) == 1:
                break

            # Ищем операцию с максимальным рангом
            pos = -1
            for i in range(len(sub_expr)):
                if sub_expr[i].content == '+' or sub_expr[i].content == '-':
                    pos = i
                    break
            for i in range(len(sub_expr)):
                if sub_expr[i].content == '*' or sub_expr[i].content == '/':
                    pos = i
                    break
            for i in range(len(sub_expr)):
                if sub_expr[i].content == '^':
                    pos = i
                    break
            if pos == -1:
                raise Exception

            # Вычисляем результат найденной операции
            operation = sub_expr[pos].content
            a1 = float(sub_expr[pos - 1].get_float_content())
            a2 = float(sub_expr[pos + 1].get_float_content())
            if operation == '+':
                res = a1 + a2
            if operation == '-':
                res = a1 - a2
            if operation == '/':
                res = a1 / a2
            if operation == '*':
                res = a1 * a2
            if operation == '^':
                res = math.pow(a1, a2)

            # Записываем результат операции в подвыражение
            sub_expr[pos] = Element('number', res)
            del sub_expr[pos - 1]
            del sub_expr[pos]

        # Вписываем результат вычисления подвыражения в основное выражение
        for i in range(pos_end - pos_start):
            del expr[pos_start]
        expr[pos_start] = sub_expr[0]

        # Проверяем условие завершения вычислений
        if len(expr) == 1:
            return expr[0].get_float_content()


# Функция, выводящая справку
def get_help():
    s = """
    Программа py_calc. Автор Сергей Лебидко. 2019 г.
    Поддерживаются следующие функции:
    sin   - синус
    cos   - косинус
    tan   - тангенс
    cotan - котангенс
    abs   - абсольтное значение (модуль)
    ln    - натуральный логарифм
    log   - логарифм по основанию 2
    lg    - логарифм по основанию 10
    sqrt  - квадратный корень числа
    exp   - экспонента
    Для возведения в степень используйте знак ^
    Для выхода введите любую из команд: exit, x, quit, q 
    """
    return s
