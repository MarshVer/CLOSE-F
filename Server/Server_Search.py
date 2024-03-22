from Client.Update import sha256_hash
from Client.config import k
from Client.password_related import pseudo_random_generator


def Dsearch(CLen, ctr, st, edb):
    res = []
    j = ctr
    while j <= CLen:
        key = sha256_hash(st + b'\x00' * 32)
        if key in edb:
            value = edb[key]
            msg = bytes(b1 ^ b2 for b1, b2 in zip(value, sha256_hash(st + b'\xff' * 32)))[:32]
            rt = bytes(b1 ^ b2 for b1, b2 in zip(value, sha256_hash(st + b'\xff' * 32)))[32:]
            while rt != b' ' * 32:
                res.append(msg)
                value = edb[sha256_hash(rt + b'\x00' * 32)]
                msg = bytes(b1 ^ b2 for b1, b2 in zip(value, sha256_hash(rt + b'\xff' * 32)))[:32]
                rt = bytes(b1 ^ b2 for b1, b2 in zip(value, sha256_hash(rt + b'\xff' * 32)))[32:]
            res.append(msg)
        j = j + 1
        st = sha256_hash(st)
    return res


def Server_Search(k1, ctr, w, edb):
    res = []
    ktw = pseudo_random_generator(k1, w)  # 利用k和w生成伪随机数并转化为bytes
    stw = sha256_hash(ktw)
    for i in range(ctr):
        stw = sha256_hash(stw)
    res = Dsearch(2000, ctr, stw, edb)
    return res
