from bitarray import bitarray

child_keys = []

# чтение из файла
def read_file(filename):
    f = open(filename, 'rb')
    msg = ''
    for lines in f:
        msg += lines.decode()
    f.close()

    return msg

# запись в файл
def write_file(filename, msg):
    f = open(filename, 'wb')

    for symb in msg:
        bt = symb.encode()
        f.write(bt)

    f.close()

# Преобразование строки в строковую форму 01
def bit_encode(s: str):
    return bitarray(
        ''.join([bin(int('1' + hex(c)[2:], 16))[3:]
                 for c in s.encode('utf-8')])).to01()

# Преобразование строки из 01 в буквы
def bit_decode(s: list):
    return ''.join([chr(i) for i in [int(b, 2) for b in s]])

# Заменить отдельный блок
# block: str, 64-битная строка 01 для преобразования
# replace_table: таблица преобразования
def replace_block(block: str, replace_table: tuple):
    result = ""
    for i in replace_table:
        try:
            result += block[i - 1]
        except IndexError:
            print(i)
            raise
    return result

#  Преобразовать входную строку в двоичную форму и разделить ее на группы по 64 бит
def processing_encode_input(enter: str):
    result = []
    bit_string = bit_encode(enter)
    # Если длина не делится на 64, добавить ноль
    if len(bit_string) % 64 != 0:
        for i in range(64 - len(bit_string) % 64):
            bit_string += '0'
    for i in range(len(bit_string) // 64):
        result.append(bit_string[i * 64: i * 64 + 64])
    return result

#  Преобразовать входную строку из двоичную формы групп по 64 бит
def processing_decode_input(enter: str):
    result = []
    try:
        input_list = enter.split("0x")[1:]
        int_list = [int("0x" + i, 16) for i in input_list]
        for i in int_list:
            bin_data = str(bin(i))[2:]
            while len(bin_data) < 64:
                bin_data = '0' + bin_data
            result.append(bin_data)
        return result
    except Exception as e:
        raise

# Преобразовать 64-битный исходный ключ в 56-битный ключ и выполнить замену
# Исходный ключ DES представляет собой 64-битную строку 01, из которой 8, 16, 24, 32, 40, 48, 56, 64 бит используются в качестве битов четности.
def key_conversion(key: str):
    key = bit_encode(key)
    while len(key) < 64:
        key += '0'
    first_key = key[:64]
    key_replace_table = (
        57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
    )
    return replace_block(first_key, key_replace_table)

# Поворот для получения 16 ключей.
# Конкретный метод состоит в том, чтобы разделить 56-битный ключ на две 28-битные подстроки, а затем циклически чередовать эти две подстроки.
def spin_key(key: str):
    # 64 бит -> 56 бит
    kc = key_conversion(key)
    first, second = kc[0: 28], kc[28: 56]
    spin_table = (1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28)
    spin_keys = []
    for i in range(16):
        first_after_spin = first[spin_table[i]:] + first[:spin_table[i]]
        second_after_spin = second[spin_table[i]:] + second[:spin_table[i]]
        spin_keys.append(first_after_spin + second_after_spin)
    return spin_keys

# Получить 48-битный подключ, выбрав перестановку
def key_selection_replacement(key: str):
    key_select_table = (
        14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
    )
    spin_keys = spin_key(key)
    for child_key56 in spin_keys:
        child_keys.append(replace_block(child_key56, key_select_table))

# Выполнить замену начального состояния на блоке
def initreplace_block(block: str):
    replace_table = (
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    )
    return replace_block(block, replace_table)

# Конвертация конечного состояния блока
def endreplace_block(block: str):
    replace_table = (
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    )
    return replace_block(block, replace_table)

# Расширенная замена
'''
Цель расширенной замены - преобразовать 32-битную строку в 48-битную в соответствии с [Расширенной таблицей перестановок].
Фактически, это повторение некоторых битов для достижения цели путаницы. 
В частности, 32-битные данные делятся на 4 * 8 маленьких блоков, и каждый маленький блок расширяется до 6 бит.
'''
def block_extend(block: str):
    extended_block = ""
    extend_table = (
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    )
    for i in extend_table:
        extended_block += block[i - 1]
    return extended_block

# XOR
def not_or(a: str, b: str):
    result = ""
    size = len(a) if len(a) < len(a) else len(b)
    for i in range(size):
        result += '0' if a[i] == b[i] else '1'
    return result

# Замена блока S, преобразование 48-битного ввода в 32-битный вывод
def s_box_replace(block48: str) -> str:
    s_box_table = (
        (
            (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
            (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
            (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
            (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),
        ),
        (
            (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
            (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
            (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
            (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),
        ),
        (
            (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
            (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
            (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
            (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),
        ),
        (
            (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
            (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
            (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
            (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),
        ),
        (
            (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
            (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
            (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
            (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),
        ),
        (
            (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
            (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
            (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
            (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),
        ),
        (
            (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
            (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
            (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
            (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),
        ),
        (
            (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
            (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
            (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
            (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
        )
    )
    result = ""
    for i in range(8):
        row_bit = (block48[i * 6] + block48[i * 6 + 5]).encode("utf-8")
        line_bit = (block48[i * 6 + 1: i * 6 + 5]).encode("utf-8")
        row = int(row_bit, 2)
        line = int(line_bit, 2)
        data = s_box_table[i][row][line]
        no_full = str(bin(data))[2:]
        while len(no_full) < 4:
            no_full = '0' + no_full
        result += no_full
    return result

"""
         После расширения и замены сжатие S-блока выполняется на 48-битной строке 01. Состоит из двух частей:
             1. XOR с ключом
             2. Согласно таблице сжатия S-блока, 48 бит сжимаются до 32 бит.
"""
def s_box_compression(num: int, block48: str):
    resultnot_or = not_or(block48, child_keys[num])
    return s_box_replace(resultnot_or)

# Роль замены p-блока также вносит путаницу. Используется [таблица замен P-блока]. Принцип такой же, как и для других замен.
# Вернуть 32-битную строку 01 после замены блока P
def p_box_replacement(block32: str):
    p_box_replace_table = (
        16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25,
    )
    return replace_block(block32, p_box_replace_table)

'''
Функция f состоит из трех частей:

Расширенная замена
Замена S-бокса
Замена P
'''
def f_function(right: str, is_decode: bool, num: int):
    # преобразовать 32 - битную строку в 48 - битную
    right = block_extend(right)
    if is_decode:
        sbc_result = s_box_compression(15 - num, right)
    else:
        sbc_result = s_box_compression(num, right)
    return p_box_replacement(sbc_result)

'''
Процесс каждого раунда циклического шифрования:

1) Разделите 64-битный блок, полученный после замены начального состояния или последнего цикла, на левый и правый 32-битные подблоки Left и Right
2)Right преобразуется функцией f для получения 32-битной строки, эта строка подвергается операции XOR с Left, чтобы получить Right следующего раунда
3)Используйте право в этом раунде исходного видения как левое в следующем раунде
4)Склейка левого окна вправо для перехода к следующему раунду
'''
def iteration(block: str, key: str, is_decode: bool):
    # формирование ключей
    key_selection_replacement(key)
    for i in range(16):
        left, right = block[0: 32], block[32: 64]
        next_left = right
        f_result = f_function(right, is_decode, i)
        # Вывод функции f подвергается XOR с левой, чтобы получить следующий раунд справа
        right = not_or(left, f_result)
        # Сшивание, готово к следующему раунду
        block = next_left + right
    return block[32:] + block[:32]

def encode(enter: str, key: str):
    result = ""
    # Обработка входной строки в блоки длиной 64
    blocks = processing_encode_input(enter)
    for block in blocks:
        # Выполняем замену начального состояния для каждого блока
        irb_result = initreplace_block(block)
        # Выполняем 16 раундов циклического шифрования для каждого блока
        block_result = iteration(irb_result, key, is_decode=False)
        # Выполняем замену окончательного состояния для каждой детали
        block_result = endreplace_block(block_result)
        result += str(hex(int(block_result.encode(), 2)))
    return result

def decode(cipher_text: str, key: str):
    result = []
    blocks = processing_decode_input(cipher_text)
    for block in blocks:
        irb_result = initreplace_block(block)
        block_result = iteration(irb_result, key, is_decode=True)
        block_result = endreplace_block(block_result)
        for i in range(0, len(block_result), 8):
            result.append(block_result[i: i + 8])
    return bit_decode(result)


if __name__ == '__main__':
    key = "hahahha"
    filename = input("Введите название файла: ")
    msg = read_file(filename)
    encode_msg = encode(msg, key)
    print("Зашифрованное сообщение: " + encode_msg)
    write_file(filename, encode_msg)

    flag = input("Расшифровать сообщение? (y - да, n - нет):  ")
    if (flag == "y"):
        msg = read_file(filename)
        decode_msg = decode(msg, key)
        write_file(filename, decode_msg)
        print("Расшифрованное сообщение: ", decode_msg)
    else:
        pass

