import base64
from Client.password_related import generate_symmetric_key


def Setup(k):
    # 生成一个k位的随机密钥
    key = generate_symmetric_key(k)
    key = base64.b85encode(key).decode('utf-8')
    key1 = generate_symmetric_key(k)
    key1 = base64.b85encode(key1).decode('utf-8')
    # 打开或创建一个文本文件（如果不存在的话）
    with open('Client/document/setup1.txt', 'w') as file:
        # 写入数据到文件
        file.write(key)
    with open('Client/document/setup2.txt', 'w') as file:
        # 写入数据到文件
        file.write(key1)

    # 创建一个空的加密数据库EDB发送给服务器
    edb = ""
    return edb
