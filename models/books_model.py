from conf.base import get_conn


def tuples_to_dic(values):
    """
    对数据库的查询结果进行转换
    """
    result = []
    for data in values:
        result.append({
            'bookId': data[0],
            'name': data[1],
            'isbn': data[2],
            'location': data[3],
            'state': data[4],
            'publishingHouse': data[5],
            'author': data[6],
            'coverUrl': data[7],
            'intro': data[8]
        })
    return result


def add_book(book):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute('insert into book(name,isbn,state,location,author,publishingHouse,coverUrl,intro) '
                       'values(%s,%s,%s,%s,%s,%s,%s,%s)',
                       (book['name'],
                        book['isbn'],
                        book['state'],
                        book['location'],
                        book['author'],
                        book['publishingHouse'],
                        book['coverUrl'],
                        book['intro'],))
        conn.commit()
        return True, '添加书籍成功！'
    except BaseException as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def update_book(book):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute('UPDATE book '
                       'SET name=%s,isbn=%s,location=%s,author=%s,publishingHouse=%s,coverUrl=%s,intro=%s'
                       'WHERE bookId=%s',
                       (book['name'],
                        book['isbn'],
                        book['location'],
                        book['author'],
                        book['publishingHouse'],
                        book['coverUrl'],
                        book['intro'],
                        book['bookId']))
        conn.commit()
        cursor.execute('SELECT * FROM book WHERE bookId = %s', (book['bookId'],))
        conn.commit()
        value = cursor.fetchall()
        return True, tuples_to_dic(value)
    except BaseException as e:
        print(str(e))
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def search_all_book(page):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    page = int(page) * 15
    cursor.execute("SELECT * FROM book limit 15 offset %s", (page,))
    conn.commit()
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    if values:
        return tuples_to_dic(values)
    else:
        return None


def delete_book(book_id):
    delete_record_by_book_id(book_id)
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("DELETE FROM Book WHERE bookId=%s", (book_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete_record_by_book_id(book_id):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("DELETE FROM Borrow_Record WHERE bookId=%s", (book_id,))
        conn.commit()
        return True, '删除成功！'
    except BaseException as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def search_book_by_book_id(book_id):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM book WHERE bookId = %s", (book_id,))
    conn.commit()
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    if values:
        return tuples_to_dic(values)
    else:
        return None


def search_book_by_name(name, page):
    """
    检索书籍
    :param name: 查询的关键字
    :param page: 页数（start:0）
    :return:
    """
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    name = '%' + name + '%'
    page = int(page) * 15
    cursor.execute("SELECT * FROM book WHERE name like %s limit 15 offset %s", (name, page,))
    conn.commit()
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    if values:
        return tuples_to_dic(values)
    else:
        return None


def search_book_by_author(author, page):
    """
    检索书籍
    :param name: 查询的关键字
    :param page: 页数（start:0）
    :return:
    """
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    author = '%' + author + '%'
    page = int(page) * 15
    cursor.execute("SELECT * FROM book WHERE author like %s limit 15 offset %s", (author, page,))
    conn.commit()
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    if values:
        return tuples_to_dic(values)
    else:
        return None


def search_book_by_key(key, type, page):
    if type == 1:
        # ID
        return search_book_by_book_id(key)
    elif type == 0:
        # 书名
        return search_book_by_name(key, page)
    else:
        # 作者
        return search_book_by_author(key, page)


def check_book_exist(book_id):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    # 检查书本ID数据
    cursor.execute("SELECT * FROM Book WHERE bookId = %s", (book_id,))
    conn.commit()
    if cursor.fetchone():
        return True
    else:
        return False


