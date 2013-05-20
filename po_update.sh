#!/bin/bash

# Скрипт предназначен для сбора из исходного кода и шаблонов текстовых
# строк, предназначенных для перевода.

LANGUAGES="ru"
PROJECTS="src"
APPS="main accounts claims code_review comments djangobb_forum doc_comments examples forum news videos links"

if test $# -gt 0; then
    APPS=$@
fi

for lang in ${LANGUAGES}; do
    for project in ${PROJECTS}; do
        cd ${project}
        mkdir -p locale
        django-admin.py makemessages --locale ${lang}
        cd ..
        for app in ${APPS}; do
            if test -d ${project}/${app}; then
                cd ${project}/${app}
                echo "Update messages for application: ${project}.${app}"
                mkdir -p locale
                django-admin.py makemessages --locale ${lang}
                cd -
            else
                echo "Unknown application ${app}. Skipping..."
            fi
        done
    done
done

exit 0
