from spiderman.orm.engine import sess

def is_exist(table, id_):
    print(table)
    result = sess.query(table).filter(idx=id_).first()
    print(result)

    return result
