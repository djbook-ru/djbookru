wget http://oligarchy.co.uk/xapian/1.2.7/xapian-core-1.2.7.tar.gz
tar xzf xapian-core-1.2.7.tar.gz
cd xapian-core-1.2.7
./configure --prefix=${VIRTUAL_ENV} && make && make install
cd -

wget http://oligarchy.co.uk/xapian/1.2.7/xapian-bindings-1.2.7.tar.gz
tar xzf xapian-bindings-1.2.7.tar.gz
cd xapian-bindings-1.2.7
./configure --prefix=${VIRTUAL_ENV} --with-python \
    --without-php --without-ruby --without-tcl --without-csharp \
    --without-java --without-perl --without-lua && make && make install
cd -
