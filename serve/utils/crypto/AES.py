from Crypto.Cipher import AES
import base64


def pad(s):
    """
    字符串补位
    :param s: 待补位的字符串
    :return: 补位后BLOCK_SIZE = 16字节的字符串
    """
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)


def unpad(s):
    """
    去除补位
    :param s: 补位后的字符串
    :return: 去除补位后的字符串
    """
    return s[:-ord(s[len(s) - 1:])]


def encrypt(content, key, vi):
    """
    AES加密
    :param content: 待加密的字符串
    :param key: 密钥
    :param vi: 偏移量
    :return: 加密后的字符串
    """

    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))

    encrypted_bytes = cipher.encrypt(pad(content).encode('utf8'))

    encode_strs = base64.b64encode(encrypted_bytes)

    return encode_strs.decode('utf8')


def decrypt(ciphertext, key, vi):
    """
    AES解密
    :param ciphertext: 待解密的字符串
    :param key: 密钥
    :param vi: 偏移量
    :return: 解密后的字符串
    """

    encode_bytes = base64.decodebytes(ciphertext.encode('utf8'))

    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))

    text_decrypted = cipher.decrypt(encode_bytes)

    return unpad(text_decrypted).decode('utf8')
