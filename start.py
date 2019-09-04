# Типы элементов выражения
OPEN_BRACKET = ['(']
CLOSE_BRACKET = [')']
OPERATIONS = list('+-*/^')
NUMBERS = list('0123456789.')
SYMBOLS = [chr(a) for a in range(ord('a'), ord('z') + 1)]


# Класс для представления отдельных элементов выражения
class Element:

    def __init__(self, type_of_content, content):
        self.type_of_content = type_of_content
        self.content = content

    def get_float_content(self):
        return float(self.content)

    def append_to_content(self, a):
        self.content += a


# Функция проверки скобок
def bracket_analysis(e):
    level = 0
    for c in e:
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
    expr = '(' + expr + ')'
    bracket_analysis(expr)
    expr = parser(expr)


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
