from cryptography.fernet import Fernet
import json
import os


def generate_key():
    """
    Генерирует ключ для симметрического шифрования и сохраняет в файл
    """
    key = Fernet.generate_key()
    with open("env", "wb") as key_file:
        key_file.write(key)
    return key


def load_key():
    """
    Загружает файл secret.key из текущей директории
    """
    return os.environ.get('CRYPT_KEY', b'default_key')


def encrypt_message(message):
    """
    Шифрует сообщение
    """
    if type(message) is dict:
        encoded_message = json.dumps(message).encode()
    else:
        encoded_message = message.encode()
    f = Fernet(load_key())
    encrypted_message = f.encrypt(encoded_message)

    return encrypted_message


def decrypt_message(encrypted_message):
    """
    Дешифрует сообщение
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    return decrypted_message.decode()
