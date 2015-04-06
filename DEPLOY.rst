Боевой сервер
=============

Создаём конфигурацию в файле ``src/prod_settings.py``.

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
