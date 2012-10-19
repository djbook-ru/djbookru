#!/bin/bash

NAME="$1"
CONF=".${NAME}.conf"

test -f ${CONF} || exit 1
source ${CONF}

MYSQLPATH=/usr/local/bin
DF="/home/rpopov/dumps/${NAME}/`date '+%Y%m%d'`.sql"

mkdir -p "/home/rpopov/dumps/${NAME}"

# make database dump
$MYSQLPATH/mysqldump -h ${DBHOST} -u ${DBUSER}  -p${DBPASS} ${DBNAME} > $DF

# compress it
/usr/bin/bzip2 $DF

# check for old dumps, keep the last week only, the rest will be deleted
find "/home/rpopov/dumps/${NAME}" -name '*.dump.bz2' -mtime +7 -delete
exit 0
