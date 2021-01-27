from cryptography.fernet import Fernet
import json
import os


def generate_key():
    """
    Генерирует ключ для симметрического шифрования
    """
    return Fernet.generate_key()


def load_key():
    """
    Загружает ключ из переменной окружения
    """
    return os.environ.get('CRYPT_KEY', b'default_key')


def encrypt_message(message):
    """
    Шифрует сообщение
    """
    encoded_message = json.dumps(message).encode()
    f = Fernet(load_key())
    encrypted_message = f.encrypt(encoded_message).decode()
    return encrypted_message


def decrypt_message(encrypted_message):
    """
    Дешифрует сообщение
    """
    f = Fernet(load_key())
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()


# print(generate_key())
