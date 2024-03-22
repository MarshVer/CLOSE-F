from Client.Setup import Setup
from Client.config import k

# 初始化
edb = Setup(k)

# 在Server新建edb加密数据库
# 以txt格式保存文件
with open('Server/EDB.txt', 'w') as file:
    file.write(edb)
