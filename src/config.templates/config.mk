
PROJECTNAME=djbookru

OWNER=rad
GROUP=www-data

INSTALL_DJANGO_DIR=/home/rad/django.apps
HTMLS_SRC=~/devel/docbook.djangobook/HTML/djangobook

REGEXP_DEVEL_URL=http:\/\/djbookru\/

PO=$(wildcard ./locale/ru/LC_MESSAGES/*.po)
MO=$(patsubst %.po,%.mo,$(PO))

