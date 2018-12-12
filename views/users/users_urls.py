from __future__ import unicode_literals
from .users_views import (
    LoginHandle, UpdateHandle,
    InsertHandle, DeleteHandle,
    SearchAllHandle, SearchHandle
)
# 处理针对 users 相关的路由及调用类之间的路由
urls = [
    (r'login', LoginHandle),
    (r'update', UpdateHandle),
    (r'insert', InsertHandle),
    (r'delete', DeleteHandle),
    (r'search', SearchHandle),
    (r'searchAll', SearchAllHandle)
]