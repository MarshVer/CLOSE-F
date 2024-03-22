from Client.password_related import decrypt_data


def select(res, k2, k):
    db = []
    for indop in res:
        ind = decrypt_data(indop, k2)[:32]
        db.append(ind)
    return db
