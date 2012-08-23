# -*- coding: utf-8 -*-

import os


def application(environ, start_response):
    status = '200 OK'
    tpl_name = os.path.join(
        os.path.dirname(__file__),
        'under_construction.html')
    html = open(tpl_name).read()
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(html)))]
    start_response(status, response_headers)
    return [html]
