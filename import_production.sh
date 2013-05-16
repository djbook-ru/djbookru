source ./.production

ssh ${USER}@${HOST} "mysqldump -h ${DBHOST} -u ${DBUSER} -p${DBPASS} ${DBNAME} > ~/site1/dump.sql"

rsync --verbose --archive --delete ${USER}@${HOST}:site1/src/public/media ./src/public/
rsync --verbose --archive --delete ${USER}@${HOST}:site1/dump.sql ./tmp/

python manage.py dbshell << EOF
\. ./tmp/dump.sql
EOF

exit 0
