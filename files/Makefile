TOP_DIR=..

include $(TOP_DIR)/config.mk

CURRENT_INSTALL_DIR=$(INSTALL_DJANGO_DIR)/$(PROJECTNAME)/files
DJZIP=djangobook.html.v2.zip
TEMPLATES=$(wildcard *.html)
SUBDIRS=
FILES=djangobook.html.v1.zip $(DJZIP)

all: 

zip: $(DJZIP)

sendzip: $(DJZIP)
	scp $(DJZIP) caml.ru:django/djbookru/files/

sendzip1: djangobook.html.v1.zip
	scp djangobook.html.v1.zip caml.ru:django/djbookru/files/

$(DJZIP): $(HTMLS_SRC)/*.html
	set -x;
	mkdir ./zip;
	for i in `ls $(HTMLS_SRC)/*.html $(HTMLS_SRC)/toc.py`; do \
	    echo `basename $$i`; \
	    cat $$i | \
	    sed 's/^.*<body[^>]*>//' | \
	    sed 's/<\/body>.*$$//' \
	    > ./zip/`basename $$i`; \
	done;
	cd ./zip; \
	zip -m ../$(DJZIP) *.html *.py; \
	cd -; \
	rmdir ./zip; \

install: create_dir install_files install_subdirs

clean:
	rm -f *.zip *~

include $(TOP_DIR)/targets.mk
