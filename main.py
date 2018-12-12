import os

import tornado.ioloop
import tornado.web
from tornado.options import define, options
from common.url_router import include, url_wrapper

"""
common：存放公共类和方法
conf: 存放配置文件
log：存放相关日志
static：存放静态文件，如样式（CSS）、脚本（js）、图片等
templates：公用模板目录，主要存放 HTML 文件
views：视图函数，业务逻辑代码目录
main.py：Tornado 主程序入口
models.py：数据库表结构定义
"""


class Application(tornado.web.Application):
    def __init__(self):
        # 路由选择
        handles = url_wrapper([
            (r"/users/", include('views.users.users_urls')),
            (r"/books/", include('views.books.books_urls')),
            (r"/records/", include('views.records.records_urls')),
            (r"/upload/", include('views.uploads.uploads_urls'))
        ])
        # 定义 Tornado 服务器的配置项，如static/templates目录位置，debug级别等
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            cookie_secret='61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo='  # 用于cookie加密的salt
        )
        tornado.web.Application.__init__(self, handles, **settings)


if __name__ == "__main__":
    print("Tornado server is ready for service\r")
    options.parse_command_line()
    Application().listen(8000, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()
