import base64
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_symmetric_key(k):
    # 生成随机的对称密钥
    key = secrets.token_bytes(k)  # 32字节的密钥，可以根据需要调整长度
    return key


def encrypt_data(data, key):
    # 使用AES算法，ECB模式，PKCS7填充
    cipher = Cipher(algorithms.AES(base64.b85decode(key)), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # 使用PKCS7填充数据
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data)
    # 不需要填充 + padder.finalize()

    # 加密数据
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # 返回Base64编码的加密结果
    return encrypted_data


def decrypt_data(encrypted_data, key):

    # 使用AES算法，ECB模式，PKCS7填充
    cipher = Cipher(algorithms.AES(base64.b85decode(key)), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    # 解密数据
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # # 使用PKCS7去除填充
    # unpadder = padding.PKCS7(128).unpadder()
    # data = unpadder.update(decrypted_data) + unpadder.finalize()

    return decrypted_data


def pseudo_random_generator(key, seed):
    # 将键和种子拼接
    data_to_hash = f"{key}{seed}".encode('utf-8')

    # 使用 PBKDF2HMAC 进行哈希
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 生成 32 字节的伪随机数
        salt=b'salt_for_pseudo_random',  # 添加盐以增加安全性
        iterations=100000,  # 迭代次数，可根据需求调整
        backend=default_backend()
    )

    # 生成伪随机数
    pseudo_random_bytes = kdf.derive(data_to_hash)

    # # 将伪随机字节串转换为整数
    # pseudo_random_number = int.from_bytes(pseudo_random_bytes, byteorder='big')
    #
    # # 将整数归一化到 [0.0, 1.0) 范围
    # normalized_value = pseudo_random_number / (2**256)

    return pseudo_random_bytes
