import random

ASCII = 256

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

# заполнение ротора элементами ASCII-кода
def new_rotor():
    rotor = [None for _ in range(ASCII)]

    cur_num = 0
    while None in rotor:
        index = random.randint(0, ASCII - 1)
        if rotor[index] == None:
            rotor[index] = cur_num
            cur_num += 1

    return rotor

# заполнение рефлектора элементами ASCII-кода
def new_reflector():
    reflector = [None for _ in range(ASCII)]
    mas = [x for x in range(ASCII)]

    for i in range(ASCII):
        if reflector[i] == None:
            num = random.choice(mas)
            while num == i:
                num = random.choice(mas)
            mas.pop(mas.index(num))
            mas.pop(mas.index(i))
            reflector[i] = num
            reflector[num] = i

    return reflector

# прогон
def encrypt(s, rotor1, rotor2, rotor3, reflector):
    s1 = rotor1.index(s)
    s2 = rotor2.index(s1)
    s3 = rotor3.index(s2)
    s4 = reflector.index(s3)
    s5 = rotor3[s4]
    s6 = rotor2[s5]
    s7 = rotor1[s6]

    return s7

# шифрование
def encrypt_message(msg, rotor1, rotor2, rotor3, reflector):
    nums = [ord(c) for c in msg]
    res_msg = []
    shift1 = 0
    shift2 = 0
    shift3 = 0
    for s in nums:
        res_msg.append(encrypt(s, rotor1, rotor2, rotor3, reflector))
        if shift1 < ASCII:
            rotor1 = rotor1[1:] + rotor1[:1]
            shift1 += 1
        elif shift2 < ASCII:
            rotor1 = rotor1[1:] + rotor1[:1]
            rotor2 = rotor2[1:] + rotor2[:1]
            shift1 = 0
            shift2 += 1
        elif shift3 < ASCII:
            rotor1 = rotor1[1:] + rotor1[:1]
            rotor2 = rotor2[1:] + rotor2[:1]
            rotor3 = rotor3[1:] + rotor3[:1]
            shift1 = 0
            shift2 = 0
            shift3 += 1
        else:
            rotor1 = rotor1[1:] + rotor1[:1]
            rotor2 = rotor2[1:] + rotor2[:1]
            rotor3 = rotor3[1:] + rotor3[:1]
            shift1 = 0
            shift2 = 0
            shift3 = 0

    return ''.join([chr(c) for c in res_msg])

def main():
    rotor1 = new_rotor()
    rotor2 = new_rotor()
    rotor3 = new_rotor()
    reflector = new_reflector()

    filename = input("Введите название файла: ")
    msg = read_file(filename)
    msg_enigma = encrypt_message(msg, rotor1, rotor2, rotor3, reflector)
    write_file(filename, msg_enigma)
    print("Зашифрованное сообщение: ", msg_enigma)
    print("Зашифрованное сообщение записано в файл")

    flag = input("Расшифровать сообщение? (y - да, n - нет):  ")
    if (flag == "y"):
        msg = read_file(filename)
        msg_secured = encrypt_message(msg, rotor1, rotor2, rotor3, reflector)
        write_file(filename, msg_secured)
        print("Расшифрованное сообщение: ", msg_secured)
    else:
        pass


if __name__ == '__main__':
    main()