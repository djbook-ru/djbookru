#!/bin/bash

# Скрипт предназначен для компиляции переводов.

PROJECTS="src"
APPS="main djangobb_forum"

if test $# -gt 0; then
    APPS=$@
fi

for project in ${PROJECTS}; do
    for app in ${APPS}; do
        if test -d ${project}/${app}; then
            cd ${project}/${app}
            echo "Compile messages for application: ${project}.${app}"
            django-admin.py compilemessages
            cd -
        else
            echo "Unknown application ${app}. Skipping..."
        fi
    done
done

exit 0
