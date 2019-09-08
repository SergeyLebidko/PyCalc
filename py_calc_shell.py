from py_calc import calculate, get_help

# Начало выполнения программы
while True:
    e = input('Введите выражение: ')
    e = e.lower().replace(' ', '')
    if e == '':
        continue
    if e == 'help' or e == '?':
        print(get_help())
        continue
    if e == 'quit' or e == 'q' or e == 'exit' or e == 'x':
        break
    try:
        # Вычисляем и выводим результат
        result = calculate(e)
        print(result)
    except Exception:
        print('Не удалось вычислить значение выражения')
