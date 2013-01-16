Совместная работа
=================

Важно!
------

Вместо TAB надо использовать 4 пробела.

Строки должны завершаться как в UNIX.

Содержимое ``~/.gitattributes``::

    *.c     filter=treatspaces
    *.txt   filter=treatspaces
    *.py    filter=treatspaces
    *.html  filter=treatspaces
    *.css   filter=treatspaces
    *.js    filter=treatspaces

Настройка атрибутов в ``~/.gitconfig``::

    [core]
        attributesfile = /home/rad/.gitattributes
    [filter "treatspaces"]
        smudge = expand -t4
        clean = expand -t4

Ветки
-----

Работа ведётся в ветках.

Узнать текущую ветку::

    git branch

Перейти на нужную ветку::

    git checkout BRANCH


Коммиты
-------

Перед коммитом всегда смотреть, что коммитится с помощью::

    git diff

Формат комментария к коммиту:

    git commit -m "Re #NNN: COMMENT."

где ``NNN`` -- номер бага в трекере, ``COMMENT`` -- текст комментария.


Репозиторий
-----------

Получать данные из репозитория так:

    git pull --rebase origin BRANCH

причём текущая ветка и BRANCH должны совпадать.

Перед отправкой своих данных в репозиторий всегда выполнять вышеприведённую команду.

Для отправки данных в репозитарий делаем так:

    git push origin BRANCH

причём текущая ветка и BRANCH должны совпадать.
