from __future__ import unicode_literals
from .uploads_views import (
    UploadImageHandle
)

urls = [
    #从/upload/file过来的请求，将调用upload_views里面的UploadFileHandle类
    (r'image', UploadImageHandle)
]