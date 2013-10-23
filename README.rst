Требования
==========

Руками надо поставить: ``python2.7``, ``virtualenv``, ``sqlite3``.

Установка
=========

Получаем исходный код проекта::

    git clone git@github.com:RaD/djbookru.git

Создаём и наполняем окружение
-----------------------------

Выполняем::

    virtualenv --python=python2.7 --system-site-packages env    # начиная с версии 1.7
    virtualenv --python=python2.7 env                           # до версии 1.7

    PIP_CACHE="~/cache/pip"
    mkdir -p ${PIP_CACHE}
    alias pipi="pip install --download-cache=${PIP_CACHE}"
    alias pipu="pip install -U --download-cache=${PIP_CACHE}"

    pipi -r ./reqs/base.txt
    pipi -r ./reqs/dev.txt

Конфигурация проекта
--------------------

Скопируйте настройки из ``src/local_settings.py.dev.template`` в
``local_settings.py``.

Изучите файл ``src/settings.py``. Необходимые правки выполните в файле
``src/local_settings.py``, который будет подгружаться при чтении
настроек проекта.

Подготовка базы данных
----------------------

Для создания/сброса SQLite базы данных для разработки используйте::

    python manage.py reset_staging

Будет создана база данных, загружены тестовые данные, создан
суперпользователь с логин/email/пароль - admin/admin@admin.com/admin,
также пользователь test/test@test.com/test

Запуск
------

При разработке мы пользуемся всей мощью ``devserver`` + ``werkzeug``::

    python manage.py runserver --werkzeug


Разработка
==========

Настройка отправки писем в консоль
----------------------------------

Добавляем в local_settings.py::

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

Миграции
--------

Новое приложение регистрируется так::

    python manage.py schemamigration APP_NAME --initial
    python manage.py migrate APP_NAME --fake 0001

Обновление тестовых фикстур
---------------------------

Если необходимо обновить тестовые (staging) фикстуры, внесите
необходимые изменения и сохраните необходимые модели используя команду
``save_staging``, пример смотрите в документации
https://github.com/code-on/django-staging

Тестирование
------------

Тестирование должно проводится перед выполнением передачи набора
коммитов в удалённый репозиторий. Тестирование выполняется с помощью
запуска одной из следующих команд::

    ./testing.sh APP_NAME
    ./testing.sh APP_NAME.CLASS_NAME.METHOD_NAME

Добавить документацию и комментарии к ней
-----------------------------------------

Для этого клонируем репозиторий документации
https://github.com/Alerion/django_documentation. Собираем её и
создаем симлинк в папку static проекта, настройки уже указаны в
local_settings.py.dev.template. Пример команды::

    ln -s ~/Workspace/django_documentation/_build/html/ ~/Workspace/djbookru/src/static/html


База данных
-----------

Создание графической модели::

    python manage.py graph_models -e -a -g > models.dot
    dot -Tsvg models.dot > models.svg
    google-chrome models.svg


Продуктив
=========

Создаём продуктивную конфигурацию в файле ``src/prod_settings.py``.

Синхронизируем проект на продуктив::

    ./deploy.sh


Виртуальное окружение
---------------------

Создаём окружение::

    mkdir -p ~/.local/lib/python2.7/site-packages

    easy_install-2.7 --prefix=~/.local virtualenv
    easy_install-2.7 --prefix=~/.local pip

    export PATH=~/.local/bin/:$PATH

Наполняем окружение::

    cd ${PATH_TO_SITE}

    virtualenv --python=python2.7 --system-site-packages env    # начиная с версии 1.7
    virtualenv --python=python2.7 env                           # до версии 1.7

    ./env/bin/pip install -r ./reqs/base.txt


Настройка Apache
----------------

Передаём управление сайтом Django::

    AddDefaultCharset utf-8
    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^\/static\/
    RewriteCond %{REQUEST_URI} !^\/media\/
    RewriteRule ^(.*)$ /webapp/$1 [L,QSA]


Дополнительное ПО
-----------------

Установка поискового движка::

    cd ~/tmp
    nice -n 19 bash ${PATH_TO_SITE}/addon/xapian_install.sh
    rm -rf ./xapian*
    cd -
    ./manage.py rebuild_index

Настройка статики::

    cd ${PATH_TO_SITE}
    . ./env/bin/activate
    python manage.pyc collectstatic
    ln -s ~/site1/src/public/static/ ~/www/site1/public_html/static
    ln -s ~/site1/src/public/media/ ~/www/site1/public_html/media


База данных
-----------

Инициализация базы данных::

    python manage.pyc syncdb --migrate --noinput
    echo "delete from django_content_type;" | python manage.pyc dbshell
    echo "delete from auth_permission;" | python manage.pyc dbshell
    python manage.pyc dbshell
    \. DUMP.sql

Возможно понадобится имитация миграций для зависимостей::

    python manage.pyc migrate admin_tools.dashboard --fake
    python manage.pyc migrate admin_tools.menu --fake
    python manage.pyc migrate easy_thumbnails --fake


Запуск
------

Активируем сайт::

    cp ${PATH_TO_SITE}/src/wsgi.py ${PATH_TO_WWW}/webapp/webapp.wsgi


Сопровождение
=============

Читаем помощь::

    $ ./deploy.sh

    Usage: deploy.sh [<command> [<command> ...]]

    where <command> is:
            * pipi    -- install packages into virtual environment;
            * pipu    -- update packages of virtual environment;
            * rsync   -- send source code to a server;
            * po      -- compile PO resources;
            * migrate -- run migrations on the database;
            * static  -- collect static files;
            * i18n    -- update multilanguage fields;
            * index   -- rebuild search index;
            * touch   -- restart web server.
