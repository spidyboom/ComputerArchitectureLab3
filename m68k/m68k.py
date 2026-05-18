def format_string(input):
    """Форматирует строку с плейсхолдерами %d, заменяя их целыми числами из входных данных.

    Формат ввода: "format_string\\nint1\\nint2\\n..."
    Примеры:
    - "Foo %d bar %d\\n232\\n43\\n" -> "Foo 232 bar 43"
    - "%5d\\n42\\n" -> "   42" (выравнивание вправо, 5 символов)
    - "%-5d\\n42\\n" -> "42   " (выравнивание влево, 5 символов)
    - "Just text\\n" -> "Just text" (без форматирования)

    Ограничение размера буфера строки формата: 0x20 байт
    Вывод: без ограничения размера

    Обработка целых чисел: принимает только 32-битные знаковые целые числа (-2147483648 до 2147483647).
    Возвращает -1, если любое целое число выходит за пределы этого диапазона.

    Возвращает отформатированную строку или коды ошибок:
    - -1 для неверного формата ввода или превышения размера строки формата 0x20 байт
    """
    try:
        lines = input.split("\n")
        if len(lines) < 1:
            return [-1], input

        format_str = lines[0]

        # Проверка ограничения размера буфера строки формата (0x20 байт)
        format_bytes = 0
        overflow_idx = None
        for idx, ch in enumerate(format_str):
            format_bytes += len(ch.encode("utf-8"))
            if format_bytes > 0x20:
                overflow_idx = idx
                break
        if overflow_idx is not None:
            remaining = input[overflow_idx + 1 :]
            return [-1], remaining

        # Найти все спецификаторы формата: %d, %5d, %-5d и т.д.
        format_specs = []
        i = 0
        while i < len(format_str):
            if format_str[i] == "%":
                spec_start = i
                i += 1
                if i < len(format_str) and format_str[i] == "-":
                    i += 1
                while i < len(format_str) and format_str[i].isdigit():
                    i += 1
                if i < len(format_str) and format_str[i] == "d":
                    format_specs.append(format_str[spec_start : i + 1])
                    i += 1
                else:
                    i = spec_start + 1
            else:
                i += 1
        placeholder_count = len(format_specs)

        # Проверить, достаточно ли строк для плейсхолдеров
        if placeholder_count > 0 and len(lines) < placeholder_count + 1:
            return [-1], input

        # Разобрать целые числа из оставшихся строк
        integers = []
        line_idx = 1
        for _ in range(placeholder_count):
            if line_idx >= len(lines):
                return [-1], input

            line = lines[line_idx]
            pos = 0
            sign = 1
            value = 0

            if pos < len(line) and line[pos] == "-":
                sign = -1
                pos += 1
            elif pos < len(line) and line[pos] == "+":
                pos += 1

            digit_start = pos

            while pos < len(line) and line[pos].isdigit():
                digit = ord(line[pos]) - ord("0")
                value = value * 10 + digit
                pos += 1

                # Проверка 32-битной границы
                if sign == 1:
                    if value > 2147483647:
                        remaining = "\n".join([line[pos:]] + lines[line_idx + 1 :])
                        return [-1], remaining
                else:
                    if value > 2147483648:
                        remaining = "\n".join([line[pos:]] + lines[line_idx + 1 :])
                        return [-1], remaining

            if digit_start == pos:
                # Проверка, пустая ли строка (отсутствуют входные данные) или недопустима
                if pos < len(line):
                    # Непустая недопустимая строка - пропустить недопустимый символ и вернуть остаток
                    remaining = "\n".join([line[pos + 1 :]] + lines[line_idx + 1 :])
                else:
                    # Пустая строка - пропустить её и вернуть остаток
                    remaining = (
                        "\n".join(lines[line_idx + 1 :])
                        if line_idx + 1 < len(lines)
                        else ""
                    )
                return [-1], remaining

            if pos < len(line):
                # Непустая недопустимая строка - пропустить недопустимый символ и вернуть остаток
                remaining = "\n".join([line[pos + 1 :]] + lines[line_idx + 1 :])
                return [-1], remaining

            parsed_int = sign * value
            integers.append(parsed_int)
            line_idx += 1

        # Форматирование строки
        try:
            if placeholder_count == 0:
                result = format_str
            else:
                result = format_str % tuple(integers)
        except (TypeError, ValueError):
            # Вычислить оставшиеся входные данные
            remaining = "\n".join(lines[line_idx:]) if line_idx < len(lines) else ""
            return [-1], remaining

        # Вычислить оставшиеся входные данные
        consumed_lines = line_idx
        if consumed_lines < len(lines):
            remaining = "\n".join(lines[consumed_lines:])
        else:
            remaining = ""

        return result, remaining

    except Exception:
        return [-1], input


assert format_string('Num: %d\n42\n') == ('Num: 42', '')
assert format_string('%5d\n42\n') == ('   42', '')
assert format_string('%-5d\n42\n') == ('42   ', '')