import argparse
import sys
from Cryptodome import *
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15 # схема цифровой подписи на основе RSA

def sign(data):
    # Получаем хэш файла
    hash = SHA256.new(data)
    # Генерируем ключи
    # биты - длина ключа. Он должен быть не менее 1024, но рекомендуется 2048
    keys = RSA.generate(2048)

    # Подписывание - шифрование данных закрытым ключом
    signature = pkcs1_15.new(keys).sign(hash)

    # Записываем подпись в файл
    sign_file = open('signature.sig', 'wb')
    sign_file.write(signature)
    sign_file.close()

    # Записываем открытый ключ в файл
    public_key = keys.publickey()
    public_key_file = open('public_key.cer', 'wb')
    public_key_file.write(public_key.exportKey())
    public_key_file.close()


def check(data):
    # Получаем хэш файла
    hash = SHA256.new(data)

    # Получаем открытый ключ
    public_key_file = open('public_key.cer', 'rb')
    public_key = RSA.import_key(public_key_file.read())

    # Считываем подпись
    signature = open('signature.sig', 'rb').read()

    # Сравниваем
    try:
        # проверка действительности подписи
        # pkcs1_15.new - создание объекта подписи для создания или проверки подписей
        # расшифровка подписи открытым ключом (расшифровка файла с хешем открым ключом)
        pkcs1_15.new(public_key).verify(hash, signature)
        print("Подпись подлинная")
    except (ValueError, TypeError):
        print("Подпись не подлинная")


if __name__ == '__main__':
    with open("lr_7_Прохорова.pdf", 'rb') as input_file:
        data = input_file.read()
        sign(data)
        print("Электронная подпись была поставлена")
        check(data)