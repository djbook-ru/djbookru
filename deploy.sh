source ./.production
export DBHOST DBNAME DBUSER DBPASS

BUILD=./build
SRC=${BUILD}/src

mkdir -p ${BUILD}

./po_compile.sh
cd src; django-admin.py compilemessages; cd -

cp -r ./addon ./lib ./reqs ./src ./manage.py ./logs ${BUILD}

rm -rf ${SRC}/{legacy,public,search/{whoosh,xapian}_index,local_settings.py,*sqlite}
rm -rf ${BUILD}/logs/*

mv ${SRC}/prod_settings.py ${SRC}/local_settings.py

find ${BUILD} -type f \
    -name '*.py' \
    -and ! -name 'wsgi.py' \
    -and ! -wholename '*/migrations/*.py' \
    -and ! -wholename '*/commands/*.py' \
    -exec py_compilefiles {} \; \
    -delete

find ${SRC} -type f -name '*.po' -delete

echo "Rsync project with ${USER}@${HOST}:${CODE_DIR}"
rsync --stats --archive --recursive --update ${BUILD}/* ${USER}@${HOST}:${CODE_DIR}/

FAB="fab production deploy_server"
DELIM=":"
for param in $@; do
    if test 'migrate' = ${param}; then
        FAB="${FAB}${DELIM}migrate=True"
        DELIM=","
    fi
    if test 'static' = ${param}; then
        FAB="${FAB}${DELIM}static=True"
        DELIM=","
    fi
    if test 'i18n' = ${param}; then
        FAB="${FAB}${DELIM}i18n=True"
        DELIM=","
    fi
    if test 'haystack' = ${param}; then
        FAB="${FAB}${DELIM}haystack=True"
        DELIM=","
    fi
    if test 'noapply' = ${param}; then
        FAB="${FAB}${DELIM}touch=False"
        DELIM=","
    fi
done
${FAB}

rm -rf ${BUILD}
