
import tornado.web
import logging
from logging.handlers import TimedRotatingFileHandler

# 从commons中导入http_response方法
from common.commons import (
    http_simple_response,http_params_error_response,
    http_error_simple_response,http_ok_simple_response
)

# 从配置文件中导入错误码
from conf.base import (
    ERROR_CODE,OK_CODE
)

from models.users_model import (
    User, login,
    save_info,search_all_user,
    search_user, delete_user,
    insert_user,

)


########## Configure logging #############
logFilePath = "log/users/users.log"
logger = logging.getLogger("Users")
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


# user的登录、注册等操作真正的逻辑处理的地方
class LoginHandle(tornado.web.RequestHandler):
    """handle /user/login request
        get:
            non_params
        post:
            userId:帐号
            password:密码
            type:帐号类型，0为读者，1为管理员

    """

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('user_id')

    def post(self):
        try:
            # 获取入参
            user_id = self.get_argument('userId')
            password = self.get_argument('password')
            type = self.get_argument('type')
        except:
            # 获取入参失败时，抛出错误码及错误信息
            logger.info("LoginHandle: request argument incorrect")
            http_simple_response(self, ERROR_CODE, "获取参数失败！")
            return
        self.set_secure_cookie('userId', user_id)
        ex_user = login(user_id, password)
        if ex_user:
            self.set_secure_cookie('userId', user_id)
            http_simple_response(self, OK_CODE, '登陆成功！', ex_user)
            return

        else:
            # 帐号或密码错误
            logger.debug("LoginHandle: account or password is error, user: %s" % user_id)
            http_simple_response(self, ERROR_CODE, "账号或密码错误！")


class UpdateHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def post(self):
        try:
            user_id = self.get_argument('userId')
            name = self.get_argument('name')
            sex = self.get_argument('sex')
            major = self.get_argument('major')
            password = self.get_argument('password')
        except:
            return http_params_error_response(self)
        user = {
            'name': name,
            'userId': user_id,
            'sex': sex,
            'major': major,
            'password': password
        }
        user = save_info(user)
        if user:
            http_simple_response(self, OK_CODE, '个人信息更新成功！', user)
        else:
            http_error_simple_response(self, '个人信息更新失败！')


class InsertHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def post(self):
        if self.get_current_user() is None:
            return http_error_simple_response(self,'权限不足！')
        try:
            user_id = self.get_argument('userId')
            name = self.get_argument('name')
            sex = self.get_argument('sex')
            major = self.get_argument('major')
            password = self.get_argument('password')
        except:
            http_params_error_response(self)
            return
        user = {
            'user_id': user_id,
            'name': name,
            'sex': sex,
            'major': major,
            'password': password,
        }
        result = insert_user(user)
        if result[0]:
            http_ok_simple_response(self, result[1])
        else:
            http_error_simple_response(self, result[1])


class DeleteHandle(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self):
        if self.get_current_user() is None:
            return http_error_simple_response(self, '权限不足！')
        try:
            user_id = self.get_argument('userId')
        except:
            http_params_error_response(self)
            return
        if delete_user(user_id):
            http_ok_simple_response(self, '删除读者成功！')
            logging.debug('删除读者成功！')
        else:
            http_error_simple_response(self, '删除读者失败！')


class SearchHandle(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self):
        if self.get_current_user() is None:
            return http_error_simple_response(self, '权限不足！')
        try:
            user_id = self.get_argument('userId')
        except:
            http_params_error_response(self)
            return
        flag, user = search_user(user_id)
        if flag:
            http_simple_response(self, OK_CODE, '搜索成功！', user)
        else:
            http_error_simple_response(self, '搜索读者失败！')



class SearchAllHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('userId')

    def get(self):
        if self.get_current_user() is None:
            return http_error_simple_response(self, '权限不足！')
        try:
            page = self.get_argument('page')
        except:
            http_params_error_response(self)
            return
        flag, users = search_all_user(page)
        if flag:
            http_simple_response(self, OK_CODE, '搜索成功！', users)
        else:
            http_error_simple_response(self, '搜索读者失败！')
