from conf.base import get_conn


class User:
    def __init__(self):
        self.user_id = ''
        self.password = ''
        self.name = ''
        self.major = ''
        self.sex = ''


def tuple_to_user(value):
    return {
        'userId': value[0],
        'password': value[1],
        'name': value[2],
        'permission': value[3],
        'sex': value[4],
        'major': value[5]
    }


def tuples_to_users(values):
    users = []
    for value in  values:
        users.append({
            'userId': value[0],
            'password': value[1],
            'name': value[2],
            'permission': value[3],
            'sex': value[4],
            'major': value[5]
        })
    return users


def login(user_id, password=None):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    if password:
        cursor.execute('SELECT * FROM User '
                       'WHERE userId = %s AND password=%s', (user_id, password))
    else:
        cursor.execute('SELECT * FROM User '
                       'WHERE userId = %s', (user_id,))
    conn.commit()
    value = cursor.fetchone()
    cursor.close()
    conn.close()
    if value:
        return tuple_to_user(value)
    else:
        return None


def save_info(user):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute(
            'UPDATE User '
            'SET name = %s,sex = %s,major = %s,password = %s '
            'where userId = %s',
            (user['name'], user['sex'], user['major'], user['password'], user['userId']))
        conn.commit()
    except BaseException as e:
        print(str(e))
        return None
    cursor.execute('SELECT * FROM User '
                   'WHERE userId = %s', (user['userId'],))
    value = cursor.fetchone()
    if value:
        return tuple_to_user(value)
    else:
        return None


def search_user(user_id):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("SELECT * FROM User WHERE userId = %s", (user_id,))
        conn.commit()
        value = cursor.fetchone()
        if not value:
            return True, ()
        else:
            return True, tuples_to_users([value])
    except BaseException as e:
        print(str(e))
        return False, ()
    finally:
        cursor.close()
        conn.close()


def search_all_user(page):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    offset = int(page) * 15
    try:
        cursor.execute("SELECT * FROM User limit 15 offset %s", (offset, ))
        conn.commit()
        value = cursor.fetchall()
        if not value:
            return True, ()
        else:
            return True, tuples_to_users(value)
    except:
        return False, ()
    finally:
        cursor.close()
        conn.close()


def delete_user(user_id):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    try:
        # 先删除借阅记录表中的数据
        cursor.execute("DELETE FROM Borrow_Record WHERE userId = %s", (user_id,))
        cursor.execute("DELETE FROM User WHERE userId = %s", (user_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()


def insert_user(user):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("SELECT * FROM User WHERE userId = %s", (user['user_id'],))
        conn.commit()
        value = cursor.fetchone()
        if value:
            return False, "该账号已存在！"
        cursor.execute("INSERT INTO User values(%s,%s,%s,%s,%s,%s) ",
                       (user['user_id'], user['password'], user['name'], 0, user['sex'], user['major']))
        conn.commit()
        return True, "添加用户成功！"
    except BaseException as e:
        return False, "添加用户失败！"+str(e)
    finally:
        cursor.close()
        conn.close()


def check_user_exist(user_id):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM User WHERE userId = %s", (user_id,))
    conn.commit()
    if cursor.fetchone():
        return True
    else:
        return False


if __name__ == '__main__':
    print(insert_user({
        'user_id': '100',
        'password': '123456',
        'major': '随机',
        'sex': '男',
        'name': 'text'
    }))
