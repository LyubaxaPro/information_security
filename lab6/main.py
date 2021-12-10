import os

def compress(data, f_comp):
    # 8-битные группы дают 256 возможных комбинации бит
    # стандартный набор символов (все возможные символы)
    # Остальные коды соответствуют обрабатываемым алгоритмом строкам.
    # bytes принимает список чисел от 0 до 255, и возвр. байты, получающ. применением ф-ии chr.
    # chr() - символ, соответствующий числу из таблицы Unicode
    dictionary = dict([(bytes([i]), i) for i in range(256)]) 

    # когда в словаре появится 256-е слово, алгоритм должен перейти к 9-битным группам
    # при появлении 512-ого слова - переход к 10-битным группам, => возможность запоминать уже 1024
    max_index = 256
    bit_width = 9
    string = bytes() # строка
    packed_bytes = ""

    for symbol in data:
        curr_byte = bytes([symbol])
        # LZW проверяет, является ли строка известной, если да -  выводит существующий код без генерации нового.
        # если строка + символ в таблице строк
        if string + curr_byte in dictionary:
            # строка = строка + символ
            string += curr_byte
        else:
            # выдать код для строки
            # bin - преобразует целое число в двоичную строку ('0b')
            bin_value = bin(dictionary[string])[2:]
            # добавить в таблицу строк строка + символ
            # чтобы размер = bit_width
            packed_bytes += '0' * (bit_width - len(bin_value)) + bin_value
            dictionary[string + curr_byte] = max_index

            if len(bin(max_index)[2:]) > bit_width:
                bit_width += 1

            max_index += 1
            # строка = символ
            string = curr_byte

    # вывести в выходной поток код для строки
    bin_value = bin(dictionary[string])[2:]
    packed_bytes += '0' * (bit_width - len(bin_value)) + bin_value

    if len(packed_bytes) % 8 != 0:
        packed_bytes += '0' * (8 - len(packed_bytes) % 8)

    # Bytearray - массив байт, является изменяемым.
    output = bytearray()
    for symbol in range(0, len(packed_bytes), 8):
        # int('', 2) - возврат числа в 2с.с в виде 10с.с
        output.append(int(packed_bytes[symbol : symbol + 8], 2))

    f_comp.write(output)


def decompress(data, f_decomp):
    dictionary = dict([(i, bytes([i])) for i in range(256)])
    next_index = 256
    bit_width = 9
    position = 0
    result = bytearray()

    data_bin_str = ""
    for i in data:
        # убираем '0b'
        bin_i = bin(i)[2:]
        data_bin_str += '0' * (8 - len(bin_i)) + bin_i

    # первый код декодируемого сообщения X
    key = int(data_bin_str[position:position + bit_width], 2)
    # первый символ
    sequence = dictionary[key]
    result.extend(sequence)
    position += bit_width

    while position + bit_width <= len(data_bin_str):
        # Считать очередной код Y из сообщения 
        key = int(data_bin_str[position:position + bit_width], 2)
        if key in dictionary:
            # получить строку
            current = dictionary[key]
        elif key == next_index:
            current = sequence + bytes([sequence[0]])

        result.extend(current)
        # добавить в таблицу фразу с кодом XY
        dictionary[next_index] = sequence + bytes([current[0]])

        next_index += 1
        position += bit_width
        if len(bin(next_index)[2:]) > bit_width:
            bit_width += 1

        # X = Y
        sequence = current

    f_decomp.write(result)


def main():
    filename = 'test.zip'
    file_compressed = 'compressed_' + filename
    file_decompressed = 'decompressed_' + filename

    with open(filename, 'rb') as f, open(file_compressed, 'wb') as f_comp:
        content = f.read()
        compress(content, f_comp)

    with open(file_compressed, 'rb') as f_comp, open(file_decompressed, 'wb') as f_decomp:
        content = f_comp.read()
        decompress(content, f_decomp)

    print("Original file: '{}' - {} bytes".format(filename, os.path.getsize(filename)))
    print("Compressed file: '{}' - {} bytes".format(file_compressed, os.path.getsize(file_compressed)))
    print("Decompressed file: '{}' - {} bytes".format(file_decompressed, os.path.getsize(file_decompressed)))


if __name__ == '__main__':
    main()