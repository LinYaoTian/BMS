import tornado.web
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import json

# 从commons中导入http_response及save_files方法
from common.commons import (
    http_simple_response,http_error_simple_response,
    http_params_error_response,http_ok_simple_response,
    save_files
)

# 从配置文件中导入错误码
from conf.base import (
    ERROR_CODE,
    OK_CODE,
    SERVER_HEADER
)

########## Configure logging #############
logFilePath = "log/uploads/upload.log"
logger = logging.getLogger("Upload")
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(logFilePath,
                                   when="D",
                                   interval=1,
                                   backupCount=30)
formatter = logging.Formatter('%(asctime)s \
%(filename)s[line:%(lineno)d] %(levelname)s %(message)s', )
handler.suffix = "%Y%m%d"
handler.setFormatter(formatter)
logger.addHandler(handler)


class UploadImageHandle(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def post(self, *args, **kwargs):
        try:
            # 获取入参
            image_metas = self.request.files['image']
        except:
            # 获取入参失败时，抛出错误码及错误信息
            logger.info("UploadFileHandle: request argument incorrect")
            http_params_error_response(self)
            return
        image_url = ""
        image_path_list = []
        if image_metas:
            # 获取当前的路径
            pwd = os.getcwd()
            save_image_path = os.path.join(pwd, "static/image/")
            logger.debug("UploadFileHandle: save image path: %s" % save_image_path)
            # 调用save_file方法将图片数据流保存在硬盘中
            file_name_list = save_files(image_metas, save_image_path)
            image_path_list = [SERVER_HEADER + "/static/image/" + i for i in file_name_list]
            ret_data = {"imageUrl": image_path_list}
            # 返回图片下载地址给客户端
            http_simple_response(self, OK_CODE, "图片上传成功！", ret_data)
        else:
            # 如果图片为空，返回图片为空错误信息
            logger.info("UploadFileHandle: image stream is e...")