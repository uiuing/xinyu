from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64


def encrypt(data, public_key):
    """
    Encrypts data with RSA public key
    :param data: data to encrypt
    :param public_key: public key
    :return: encrypted data
    """
    cipher = PKCS1_v1_5.new(RSA.importKey(public_key))
    cipher_text = base64.b64encode(cipher.encrypt(data.encode()))
    return cipher_text.decode()


def decrypt(cipher_text, private_key):
    """
    Decrypts data with RSA private key
    :param cipher_text: data to decrypt
    :param private_key: private key
    :return: decrypted data
    """
    cipher = PKCS1_v1_5.new(RSA.importKey(private_key))
    message = cipher.decrypt(base64.b64decode(cipher_text), 'ERROR')
    return message.decode()
