import tornado.web
import logging
import os
from logging.handlers import TimedRotatingFileHandler

# 从commons中导入http_response方法
from common.commons import (
    http_simple_response,http_error_simple_response,
    http_ok_simple_response, http_params_error_response,
    save_files
)

from conf.base import (
    OK_CODE, ERROR_CODE, SERVER_HEADER
)

from models.books_model import (
    search_book_by_name, add_book, search_book_by_book_id,
    search_all_book, update_book, delete_book, search_book_by_key
)


########## Configure logging #############
logFilePath = "log/search/search.log"
logger = logging.getLogger("Search")
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(logFilePath,
                                   when="D",
                                   interval=1,
                                   backupCount=30,
                                   encoding='utf-8')
formatter = logging.Formatter('%(asctime)s \
%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',)
handler.suffix = "%Y%m%d"
handler.setFormatter(formatter)
logger.addHandler(handler)


class SearchByBookIdHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self):
        if not self.get_current_user():
            http_error_simple_response(self, '权限不足！')
            return
        try:
            book_id = self.get_argument('bookId')
        except:
            http_params_error_response(self)
            return
        books = search_book_by_book_id(book_id)
        http_simple_response(self, OK_CODE, '查询成功！', books)


class SearchByNameHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self):
        try:
            key = self.get_argument('key')
            page = self.get_argument('page')
        except:
            http_params_error_response(self)
            return
        books = search_book_by_name(key, page)
        http_simple_response(self, OK_CODE, '查询成功！', books)
        logger.debug("Search: search key = %s", key)


class SearchByKeyHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        try:
            key = self.get_argument('key')
            page = self.get_argument('page')
            type = self.get_argument('type')
        except:
            http_params_error_response(self)
            return
        type = int(type)
        books = search_book_by_key(key, type, page)
        if books:
            http_simple_response(self, OK_CODE, '查询成功！', books)
        else:
            http_simple_response(self, OK_CODE, '无结果！', books)
        logger.debug("Search: search key = %s", key)


class SearchAllHandle(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self):
        try:
            page = self.get_argument('page')
        except:
            http_params_error_response(self)
            return
        books = search_all_book(page)
        http_simple_response(self, OK_CODE, '查询成功！', books)
        logger.debug("Search: searchAll")


class UpdateHandle(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def post(self):
        if not self.get_current_user():
            http_error_simple_response(self, '请登录！')
            return
        try:
            book = {
                'bookId': self.get_argument('bookId'),
                'name': self.get_argument('name'),
                'isbn': self.get_argument('isbn'),
                'location': self.get_argument('location'),
                'publishingHouse': self.get_argument('publishingHouse'),
                'author': self.get_argument('author'),
                'coverUrl': self.get_argument('coverUrl'),
                'intro': self.get_argument('intro')
            }
        except:
            http_params_error_response(self)
            return
        try:
            # 获取入参
            image_metas = self.request.files['file']
        except:
            logger.info('获取图片出错！')
            image_metas = []
        if image_metas:
            # 存储图片
            pwd = os.getcwd()
            save_image_path = os.path.join(pwd, "static/image/")
            logger.debug("UploadFileHandle: save image path: %s" % save_image_path)
            # 调用save_file方法将图片数据流保存在硬盘中
            file_name_list = save_files(image_metas, save_image_path)
            image_path_list = [SERVER_HEADER + "/static/image/" + i for i in file_name_list]
            book['coverUrl'] = image_path_list[0]
        result = update_book(book)
        print(result)
        if result[0]:
            http_simple_response(self, OK_CODE, '更新书籍信息成功！', result[1])
        else:
            http_error_simple_response(self, result[1])
        logger.debug("Search: update bookId="+book['bookId'])


class DeleteHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self, *args, **kwargs):
        if not self.get_current_user():
            http_error_simple_response(self, '请登录！')
            return
        try:
            book_id = self.get_argument('bookId')
        except:
            http_params_error_response(self)
            return
        delete_book(book_id)
        http_ok_simple_response(self,'删除成功！')


class AddHandle(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def post(self, *args, **kwargs):
        if not self.get_current_user():
            http_error_simple_response(self, '请登录！')
            return
        try:
            book = {
                'name': self.get_argument('name'),
                'isbn': self.get_argument('isbn'),
                'location': self.get_argument('location'),
                'publishingHouse': self.get_argument('publishingHouse'),
                'author': self.get_argument('author'),
                'coverUrl': self.get_argument('coverUrl'),
                'intro': self.get_argument('intro'),
                'state': 0
            }
        except BaseException as e:
            http_error_simple_response(self, str(e))
            return
        try:
            # 获取入参
            image_metas = self.request.files['file']
        except:
            logger.info('获取图片出错！')
            image_metas = []
        if image_metas:
            # 存储图片
            pwd = os.getcwd()
            save_image_path = os.path.join(pwd, "static/image/")
            logger.debug("UploadFileHandle: save image path: %s" % save_image_path)
            # 调用save_file方法将图片数据流保存在硬盘中
            file_name_list = save_files(image_metas, save_image_path)
            image_path_list = [SERVER_HEADER + "/static/image/" + i for i in file_name_list]
            book['coverUrl'] = image_path_list[0]
        result = add_book(book)
        http_simple_response(self, OK_CODE if result[0] else ERROR_CODE, result[1])
        logger.debug("Search: add book")

