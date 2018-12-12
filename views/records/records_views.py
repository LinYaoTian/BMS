import tornado.web
import logging
from logging.handlers import TimedRotatingFileHandler

# 从commons中导入http_response方法
from common.commons import (
    http_simple_response, http_error_simple_response,
    http_ok_simple_response, http_params_error_response,
)

from conf.base import (
    OK_CODE, ERROR_CODE
)

from models.records_model import (
    search_all_record_by_user_id,
    insert_record, return_book,
    search_all_record_by_book_id, search_record_by_user_id,
    search_all_record
)

########## Configure logging #############
logFilePath = "log/records/record.log"
logger = logging.getLogger("record")
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(logFilePath,
                                   when="D",
                                   interval=1,
                                   backupCount=30,
                                   encoding='utf-8')
formatter = logging.Formatter('%(asctime)s \
%(filename)s[line:%(lineno)d] %(levelname)s %(message)s', )
handler.suffix = "%Y%m%d"
handler.setFormatter(formatter)
logger.addHandler(handler)


class MyRecordHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self):
        user_id = self.get_current_user()
        if not user_id:
            http_simple_response(self, ERROR_CODE, "请登陆!")
            return
        try:
            page = self.get_argument('page')
        except:
            http_simple_response(self, ERROR_CODE, "获取参数失败！")
            return
        records = search_record_by_user_id(user_id, page)
        http_simple_response(self, OK_CODE, "获取数据成功！", records)


class ReturnBookHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self):
        user_id = self.get_current_user()
        if not user_id:
            http_simple_response(self, ERROR_CODE, "请登陆!")
            return
        try:
            user_id = self.get_argument('userId')
            book_id = self.get_argument('bookId')
        except:
            http_simple_response(self, ERROR_CODE, "获取参数失败！")
            return
        result = return_book(user_id, book_id)
        http_simple_response(self,
                             OK_CODE if result[0] else ERROR_CODE,
                             result[1])


class BorrowBookHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self):
        user_id = self.get_current_user()
        if not user_id:
            http_simple_response(self, ERROR_CODE, "请登陆!")
            return
        try:
            user_id = self.get_argument('userId')
            book_id = self.get_argument('bookId')
        except:
            http_simple_response(self, ERROR_CODE, "获取参数失败！")
            return
        result = insert_record(user_id, book_id)
        http_simple_response(self,
                             OK_CODE if result[0] else ERROR_CODE,
                             result[1])


class AllRecordHandle(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self):
        user_id = self.get_current_user()
        if not user_id:
            http_simple_response(self, ERROR_CODE, "请登陆!")
            return
        try:
            page = self.get_argument('page')
        except:
            http_simple_response(self, ERROR_CODE, "获取参数失败！")
            return
        http_simple_response(self,
                             OK_CODE,
                             "",
                             search_all_record(page))


class SearchRecordHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self):
        if not self.get_current_user():
            http_simple_response(self, ERROR_CODE, "请登陆!")
            return
        try:
            key = self.get_argument('key')
            key_type = self.get_argument('type')
        except:
            http_simple_response(self, ERROR_CODE, "获取参数失败！")
            return

        result = search_all_record_by_user_id(key) if int(key_type) == 0 else search_all_record_by_book_id(key)
        http_simple_response(self, OK_CODE, "", result)

