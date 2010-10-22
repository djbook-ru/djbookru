# -*- coding: utf-8 -*-
import os, sys
sys.stdout = sys.stderr
sys.path.insert(0, os.path.dirname(__file__))
sys.path.append('/home/rad/engine')
sys.path.append('/home/rad/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core.handlers.wsgi import WSGIHandler

application = WSGIHandler()
#handler = WSGIHandler()

#def application(environ, start_response):
#    start_response('200 OK', [('Content-type', 'text/html')])
#    return """
#<html>
#  <head>
#    <title>Обновляемся</title>
#  </head>
#  <body>
#    <h1>Свершилось</h1>
#    <p>Завершена работа над сайтом.</p>
#    <p>Идёт процесс обновления.</p>
#    <p>Скоро вернёмся!</p>
#  </body>
#</html>
#"""

