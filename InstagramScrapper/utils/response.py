import csv

from django.core.files import File
from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.renderers import JSONRenderer
import pandas as pd

class CustomJSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(CustomJSONResponse, self).__init__(content, **kwargs)

class ResponseModelJson(object):
    def error(**kwargs):
        return CustomJSONResponse(dict(kwargs, success = False))

    def success(**kwargs):
        return CustomJSONResponse(dict(kwargs, success = True))



def ResponseModelCsv(file,name = 'default'):
    response = HttpResponse(file, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + name + '.csv"'
    return response


def ResponseModelXl(file_data):
    response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="foo.xls"'
    return response


def ResponseModelZip():
    response = HttpResponse(content_type='text/zip')
    response['Content-Disposition'] = 'attachment; filename=filename.zip'
    return response
