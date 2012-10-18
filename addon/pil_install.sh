DIR="jpeg-8c"
FILE="jpegsrc.v8c.tar.gz"
URL="http://www.ijg.org/files/${FILE}"
test -f ${FILE} || wget --continue ${URL}
test -d ${DIR} || tar xzf ${FILE}
cd ${DIR}
./configure --prefix=${VIRTUAL_ENV} && make && make install
cd -

DIR="zlib-1.2.7"
FILE="${DIR}.tar.gz"
URL="http://zlib.net/${FILE}"
test -f ${FILE} || wget --continue ${URL}
test -d ${DIR} || tar xzf ${FILE}
cd ${DIR}
./configure --prefix=${VIRTUAL_ENV} && make && make install
cd -

DIR="freetype-2.4.10"
FILE="${DIR}.tar.gz"
URL="http://download.savannah.gnu.org/releases/freetype/${FILE}"
test -f ${FILE} || wget --continue ${URL}
test -d ${DIR} || tar xzf ${FILE}
cd ${DIR}
./configure --prefix=${VIRTUAL_ENV} && make && make install
cd -
