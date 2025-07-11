from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import os

def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=32, count=100000)

def encrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        plaintext = f.read()

    salt = get_random_bytes(16)
    key = derive_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext))

    encrypted_data = salt + cipher.iv + ct_bytes
    encrypted_file = file_path + ".lock"

    with open(encrypted_file, 'wb') as ef:
        ef.write(encrypted_data)

    os.remove(file_path)
    return encrypted_file

def decrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        data = f.read()

    salt = data[:16]
    iv = data[16:32]
    ct = data[32:]

    key = derive_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        pt = unpad(cipher.decrypt(ct))
    except ValueError:
        return None  # wrong password

    original_path = file_path.replace(".lock", "")
    with open(original_path, 'wb') as of:
        of.write(pt)

    os.remove(file_path)
    return original_path
