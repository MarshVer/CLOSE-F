import base64
import time
from Client.config import k
from Client.password_related import decrypt_data
from Client.select import select
from Server.Server_Search import Server_Search

# 查找的关键字
key = 'hf'

# 读取密钥skey
with open('Client/document/setup1.txt', 'r') as file:
    k1 = file.read()

with open('Client/document/setup2.txt', 'r') as file:
    k2 = file.read()

# 初始化update_dict（数据库数据）
update_dict = {}

# 从文件加载update字典并保存到update_dict
with open('Server/EDB.txt', 'r') as file:
    for line in file:
        data = line.split()
        update_dict[data[0]] = data[1:]  # 提取关键字和文档id并将数据存入字典

# base64解码字典的键值对为字节串
update_dict = {base64.b85decode(key): base64.b85decode(value[0]) for key, value in update_dict.items()}

inds = []  # 初始化查找的文档索引

start_time = time.time()  # 记录开始时间
# 开始查找文档索引并保存到inds
inds = Server_Search(k1, 1999, key, update_dict)
inds = select(inds, k2, k)
end_time = time.time()  # 记录结束时间

# 初始化解密后的关键字/文档字典
dict_inds = {}
ind_ints = []       # 解密后的文档索引
# 将加密的文档索引一个一个解密并保存到ind_ints里
for ind in inds:
    ind_ints.append(int.from_bytes(decrypt_data(ind, k1), byteorder='big'))  # 解密

    dict_inds[key] = ind_ints
print('查找关键字：{0}，共找到：{1}个文档, 文档解密后为：{2}'.format(key, len(inds), ind_ints[1:]))  # 记录查找的时间
print('查找关键字：{0}，共找到：{1}个文档, 耗时：{2}s'.format(key, len(inds), end_time-start_time))  # 记录查找的时间
