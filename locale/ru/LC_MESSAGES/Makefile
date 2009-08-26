TOP_DIR=../../..

include $(TOP_DIR)/config.mk

CURRENT_INSTALL_DIR=$(INSTALL_DJANGO_DIR)/$(PROJECTNAME)/locale/ru/LC_MESSAGES
FILES=$(patsubst %.po, %.mo, $(wildcard *.po))

all:

install: create_dir install_files

clean:
	rm -f *.mo *~

locale: $(FILES)

%.mo: %.po
	cd $(TOP_DIR); \
	django-admin.py compilemessages

include $(TOP_DIR)/targets.mk
