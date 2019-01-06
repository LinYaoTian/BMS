import datetime
from conf.base import get_conn
from models.books_model import check_book_exist
from models.users_model import (
    check_user_exist
)
import time


def tuples_to_dic(values):
    """
    对数据库的查询结果进行转换
    """
    result = []
    for data in values:
        returnTime = None
        borrowTime = None
        if not data[4] is None:
            returnTime = str(data[4])
        if not data[5] is None:
            borrowTime = str(data[5])
        result.append({
            'bookId': data[0],
            'userId': data[1],
            'coverUrl': data[2],
            'bookName': data[3],
            'returnTime': returnTime,
            'borrowTime': borrowTime
        })
    print(result)
    return result


def search_record_by_user_id(user_id, page):
    """
    检索借书记录
    :param user_id:
    :param page: 页数（start:0）
    :return:
    """
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    page = int(page) * 15
    cursor.execute("SELECT borrow_record.bookId, borrow_record.userId,"
                   "coverUrl, book.name,returnTime, borrowTime "
                   "FROM book, borrow_record "
                   "WHERE userId = %s and book.bookId = borrow_record.bookId "
                   "order by borrowTime desc limit 15 offset %s", (user_id, page))
    conn.commit()
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    if values:
        return tuples_to_dic(values)
    else:
        return None


def search_all_record_by_book_id(book_id):
    """
     检索借书记录
    :param book_id:
    :return:
    """
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT borrow_record.bookId, borrow_record.userId,"
                   "coverUrl, book.name,returnTime, borrowTime "
                   "FROM book, borrow_record "
                   "WHERE borrow_record.bookId = %s and book.bookId = borrow_record.bookId ", (book_id,))
    conn.commit()
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    if values:
        return tuples_to_dic(values)
    else:
        return None


def search_all_record(page):
    """
     检索借书记录
    :param page:
    """
    """
        检索借书记录
        :param user_id:
        :param page: 页数（start:0）
        :return:
        """
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    page = int(page) * 15
    cursor.execute("SELECT borrow_record.bookId, borrow_record.userId,"
                   "coverUrl, book.name,returnTime, borrowTime "
                   "FROM book, borrow_record "
                   "WHERE book.bookId = borrow_record.bookId "
                   "order by borrowTime desc limit 15 offset %s", (page, ))
    conn.commit()
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    if values:
        return tuples_to_dic(values)
    else:
        return None


def search_all_record_by_user_id(user_id):
    """
     检索借书记录
    :return:
    """
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT borrow_record.bookId, borrow_record.userId,"
                   "coverUrl, book.name,returnTime, borrowTime "
                   "FROM book, borrow_record "
                   "WHERE userId = %s and book.bookId = borrow_record.bookId ", (user_id,))
    conn.commit()
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    if values:
        return tuples_to_dic(values)
    else:
        return None


def return_book(user_id, book_id):
    """
    还书
    :param user_id:
    :param book_id:
    :return:
    """
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if not check_user_exist(user_id):
            return False, '用户不存在！'
        if not check_book_exist(book_id):
            return False, '书本不存在！'

        # 先检查数据库是否存在该用户尚未归还的借书记录
        cursor.execute("SELECT * FROM Borrow_Record "
                       "WHERE bookId = %s AND userId = %s AND returnTime = NULL ", (book_id, user_id))
        conn.commit()
        if cursor.fetchone():
            return False, '借书记录不存在！'

        # 更新数据库
        cursor.execute("UPDATE Borrow_Record SET returnTime=%s WHERE bookId=%s and userId=%s",
                       (dt, book_id, user_id))
        cursor.execute("UPDATE Book SET state = 0 WHERE bookId=%s", (book_id,))
        conn.commit()
        return True, '还书成功！'
    except BaseException as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def insert_record(user_id, book_id):
    """
    插入借书记录
    :param user_id:
    :param book_id:
    :return:
    """
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if not check_user_exist(user_id):
            return False, '用户不存在！'
        if not check_book_exist(book_id):
            return False, '书本不存在！'

        # 先检查数据库中该书籍是否被借出
        cursor.execute("SELECT state FROM Book WHERE bookId = %s", (book_id,))
        conn.commit()
        state = cursor.fetchone()
        if state == 1:
            return False, '书籍已被借出！'
        # 插入数据
        cursor.execute("INSERT INTO Borrow_Record VALUES(%s,%s,%s,%s)",
                       (book_id, user_id, dt, None))
        cursor.execute("UPDATE Book SET state = 1 WHERE bookId=%s", (book_id,))
        conn.commit()
        return True, '借书成功！'
    except BaseException as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def delete_record_by_user_id(user_id):
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("DELETE FROM Borrow_Record WHERE bookId=%s", (user_id,))
        conn.commit()
        return True, '删除成功！'
    except BaseException as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    pass