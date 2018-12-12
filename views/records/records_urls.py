from __future__ import unicode_literals
from .records_views import (
    MyRecordHandle, AllRecordHandle,
    ReturnBookHandle, BorrowBookHandle,
    SearchRecordHandle
)
urls = [
    (r'myRecord', MyRecordHandle),
    (r'allRecord', AllRecordHandle),
    (r'return', ReturnBookHandle),
    (r'borrow', BorrowBookHandle),
    (r'search', SearchRecordHandle)
]
