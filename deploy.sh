#!/bin/bash

if [ -n "${VIRTUAL_ENV-x}" ]; then
    . env/bin/activate
    DEACTIVATE_FORCE=1
fi

ant configure

#cd src
#echo "Collect static files"
#python manage.py collectstatic --verbosity=0 --noinput
#cd -

rm -f ./project.user.properties && \
ln -s ./project.user.production ./project.user.properties

ant deploy

rm -f ./project.user.properties && \
ln -s ./project.user.development ./project.user.properties && \

ant clean configure

if [ -n "${DEACTIVATE_FORCE+x}" ]; then
    deactivate
fi
