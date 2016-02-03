.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/djbook-ru/djbookru
   :target: https://gitter.im/djbook-ru/djbookru?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

Требования
==========

Руками надо поставить: ``python2.7``, ``virtualenv``, ``sqlite3``.

Установка
=========

Получаем исходный код проекта::

    $ git clone git@github.com:RaD/djbookru.git

Создаём и наполняем окружение
-----------------------------

Выполняем::

    $ cd djbookru
    $ virtualenv --python=python2.7 env
    $ . env/bin/activate
    $ pip install -r reqs/base.txt
    $ pip install -r reqs/test.txt

Конфигурация проекта
--------------------

Скопируйте настройки ``local_settings.py``::

    $ cp src/local_settings.py.dev.template src/local_settings.py

База данных
-----------

Создаем базу данных на SQLite::

    $ python manage.py migrate

Создаем супер-пользователя командо::

    $ python manage.py createsuperuser

Запуск
------

Теперь должно работать::

    $ python manage.py runserver

Makefile
--------

Удаляем все *.pyc файлы::

    $ make clean


Дополнительно
=============

Установка поискового движка
---------------------------

Установка поискового движка::

    cd ~/tmp
    nice -n 19 bash <PATH_TO_SITE>/addon/xapian_install.sh
    rm -rf ./xapian*
    cd -
    ./manage.py rebuild_index

Тестирование
------------

Для тестирования использутся `nose <https://nose.readthedocs.org/en/latest/>`_.
Он интегрируется в Django, так что запускать тесты стандартной командой ``test``.

Добавить документацию и комментарии к ней
-----------------------------------------

Для этого клонируем репозиторий документации
https://github.com/Alerion/django_documentation. Собираем её и
создаем симлинк в папку static проекта, настройки уже указаны в
local_settings.py.dev.template. Пример команды::

    ln -s ~/Workspace/django_documentation/_build/html/ ~/Workspace/djbookru/src/static/html


.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/djbook-ru/djbookru
   :target: https://gitter.im/djbook-ru/djbookru?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
