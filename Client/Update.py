import base64
import hashlib
import json
import secrets
import struct
from Client.password_related import generate_symmetric_key, pseudo_random_generator, encrypt_data
from Client.config import k


def sha256_hash(input_bytes):
    # 创建一个 SHA-256 哈希对象
    sha256_hash_obj = hashlib.sha256()

    # 更新哈希对象
    sha256_hash_obj.update(input_bytes)

    # 获取十六进制表示的哈希值并转换为字节串
    hash_hex = sha256_hash_obj.hexdigest()

    # 将前32字节的哈希值重复三次
    hash_bytes = bytes.fromhex(hash_hex[:32] * 4)

    return hash_bytes


def DUpdate(st, dic, ind):
    key = sha256_hash(st + b'\x00' * 32)
    if key not in dic:
        value = bytes(b1 ^ b2 for b1, b2 in zip(sha256_hash(st + b'\xff' * 32), (ind + b' ' * 32)))
        dic[key] = value
    else:
        value = dic[key]
        rt = secrets.token_bytes(k)
        dic[key] = bytes(b1 ^ b2 for b1, b2 in zip(sha256_hash(st + b'\xff' * 32), (ind + rt)))
        dic[sha256_hash(rt + b'\x00' * 32)] = bytes(
            b1 ^ b2 ^ b3 for b1, b2, b3 in zip(sha256_hash(rt + b'\xff' * 32), sha256_hash(st + b'\xff' * 32), value))
    return dic


def Update(k1, k2, ctr, w, inds):
    update = {}  # 初始化空的更新字典
    kw = {}  # 初始化空的更新字典
    for ind in inds:
        if w not in kw:
            ktw = pseudo_random_generator(k1, w)  # 利用k和w生成伪随机数并转化为bytes
            stw = sha256_hash(ktw)
            for i in range(ctr):
                stw = sha256_hash(stw)
            kw[w] = stw
        stw = kw[w]
        indop = encrypt_data(ind, k2)  # 加密
        update = DUpdate(stw, update, indop)
    with open('Client/document/setup.txt', 'w') as file:
        file.writelines(k1+"\n")
        file.writelines(k2+"\n")
        file.writelines("1999" + "\n")
    return update
