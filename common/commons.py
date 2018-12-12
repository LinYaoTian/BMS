import json
import os
from conf.base import (
    OK_CODE, ERROR_CODE
)


def http_simple_response(self, code, msg, data=None):
    self.write(json.dumps(
        {"code": code,
         "msg": msg,
         "data": data}, ensure_ascii=False)
    )


def http_params_error_response(self):
    http_simple_response(self, ERROR_CODE, '参数错误！')


def http_error_simple_response(self, msg):
    http_simple_response(self, ERROR_CODE, msg)


def http_ok_simple_response(self, msg):
    http_simple_response(self, OK_CODE, msg)


def save_files(file_metas, in_rel_path, type='image'):
    """
    Save file stream to server
    """
    file_path = ""
    file_name_list = []
    for meta in file_metas:
        file_name = meta['filename']
        print('fileName:'+file_name)
        file_path = os.path.join(in_rel_path, file_name)
        print('filePath:'+file_path)
        file_name_list.append(file_name)
        #save image as binary
        with open(file_path, 'wb') as up:
            up.write(meta['body'])
    return file_name_list


# def http_login_response(self, code, msg, user):
#     data = {'userId': user.user_id, 'name': user.name, 'major': user.major, 'sex': user.sex}
#     http_simple_response(self, code, msg, data)



