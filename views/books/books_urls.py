from __future__ import unicode_literals
from .books_views import (
    SearchByKeyHandle, SearchAllHandle,
    AddHandle, UpdateHandle,DeleteHandle,SearchByBookIdHandle
)
# 处理针对 search 相关的路由及调用类之间的路由
urls = [
    (r'search', SearchByKeyHandle),
    (r'searchByBookId', SearchByBookIdHandle),
    (r'searchAll', SearchAllHandle),
    (r'update', UpdateHandle),
    (r'add', AddHandle),
    (r'delete', DeleteHandle)
]