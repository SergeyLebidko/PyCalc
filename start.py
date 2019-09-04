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
        subexpr = expr[pos_start + 1: pos_end]

        break


# Начало выполнения программы
while True:
    e = input('Введите выражение: ')
    e = e.lower().replace(' ', '')
    if e == '':
        continue
    if e == 'quit' or e == 'q' or e == 'exit' or e == 'x':
        break
    try:
        calculate(e)
    except Exception:
        print('Не удалось вычислить значение выражения')
