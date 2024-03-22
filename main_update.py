import time
import base64
from pybloom_live import ScalableBloomFilter
from Client.config import k
from Client.password_related import encrypt_data
from Client.Update import Update

# 指定本地keywords-document-index的文件路径(可包含多个关键字)
document_dict_path = 'Client/db/100.txt'
# 指定对文档的操作add/del
op = 'add'

# 读取密钥key
with open('Client/document/setup1.txt', 'r') as file:
    k1 = file.read()
with open('Client/document/setup2.txt', 'r') as file:
    k2 = file.read()


# 从文件加载数据为字典
document_dic = {}
with open(document_dict_path, 'r') as file:
    for line in file:
        # 分割每行数据
        data = line.split()
        # 提取关键字和文档id并将数据存入字典
        document_dic[data[0]] = data[1:]

# 加密关键字对应的文档索引
encrypt_dict = {}
# 加密文档索引并将其保存在encrypt_inds集合
for keyword in document_dic:
    encrypt_inds = []
    for doc_ind in document_dic[keyword]:
        encrypt_ind = encrypt_data(int(doc_ind).to_bytes(32, 'big'), k1)  # 加密
        encrypt_inds.append(encrypt_ind)
    encrypt_dict[keyword] = encrypt_inds

update = {}
# 记录开始时间
start_time = time.time()
for keyword in encrypt_dict:
    # 更新关键字问文档索引
    update.update(Update(k1, k2, 2000, keyword, encrypt_dict[keyword]))
# 记录结束时间
end_time = time.time()
print("更新Enron全部关键字和文档的时间：", end_time - start_time)

# 保存update
with open('Server/EDB.txt', 'a') as file:
    for key, value in update.items():
        # 将键值对格式化为字符串，并写入文件
        line = f"{base64.b85encode(key).decode('utf-8')}{' '}{base64.b85encode(value).decode('utf-8')}\n"
        file.write(line)
print("update保存成功")
