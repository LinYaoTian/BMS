from __future__ import unicode_literals
from .books_views import (
    SearchByNameHandle, SearchAllHandle,
    AddHandle, UpdateHandle,
    DeleteHandle, SearchByBookIdHandle,
    SearchByKeyHandle
)
# 处理针对 search 相关的路由及调用类之间的路由
urls = [
    (r'search', SearchByNameHandle),
    (r'searchByBookId', SearchByBookIdHandle),
    (r'searchAll', SearchAllHandle),
    (r'searchByKey', SearchByKeyHandle),
    (r'update', UpdateHandle),
    (r'add', AddHandle),
    (r'delete', DeleteHandle)
]