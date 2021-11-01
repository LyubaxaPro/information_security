import random
import math
from base64 import b32encode, b32decode

begin = 17
end = 1000

# проверка является ли число простым
def miller_rabin_test(n):
    k = int(math.log(n, 2) + 1)

    if (n == 2 | n == 3):
        return True

    if (n < 2 | n % 2 == 0):
        return False

    t = n - 1
    s = 0
    while (t % 2 == 0):
        t //= 2
        s += 1

    for i in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, t, n)

        if (x == 1 | x == n - 1):
            continue

        for r in range(1, s):
            x = pow(x, 2, n)
            if (x == 1):
                return False
            if (x == n - 1):
                break

        if (x != n - 1):
            return False

    return True

# поиск простого числа в пределах
def get_prime_number(begin, end, not_equal=0):
    a = random.randint(begin, end)
    t = miller_rabin_test(a)
    while not t:
        a = random.randint(begin, end)
        t = miller_rabin_test(a)
        if (a == not_equal):
            t = False
    return a

def gcd(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b


def get_e(a):
    b = random.randint(0, end)
    while (gcd(a, b) != 1):
        b = random.randint(0, end)
    return b


def get_d(e, f):
    k = 0
    while ((k * f + 1) % e != 0):
        k += 1
    return (k * f + 1) // e


def RSA_params():
    p = get_prime_number(begin, end)
    q = get_prime_number(begin, end, p)

    n = p * q
    f = (p - 1) * (q - 1)
    e = get_e(f)  # открытый (e, n)
    d = get_d(e, f)  # закрытый

    return n, e, d


def RSA(sym, n, e, d, enc=True):
    if (enc):
        return pow(sym, e, n)
    else:
        return pow(sym, d, n)


def RSA_string(string, n, e, d, enc=True):
    res = ""
    for char in string:
        ch = RSA(ord(char), n, e, d, enc)
        res += chr(ch)
    return res


def main():
    input_file = input("Input filename: ")
    file_read = open(input_file, 'rb')
    file_write_enc = open('enc_'+input_file, 'w')
    file_write_dec = open('dec_'+input_file, 'wb')

    n, e, d = RSA_params()

    data = b32encode(file_read.read())
    str = data.decode("ascii")
    str_enc = RSA_string(str, n, e, d)
    file_write_enc.write(str_enc)

    str_dec = RSA_string(str_enc, n, e, d, False)
    str = b32decode(str_dec)
    file_write_dec.write(str)

    file_read.close()
    file_write_enc.close()
    file_write_dec.close()


if __name__ == "__main__":
    main()