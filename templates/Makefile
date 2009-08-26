TOP_DIR=..

include $(TOP_DIR)/config.mk

CURRENT_INSTALL_DIR=$(INSTALL_DJANGO_DIR)/$(PROJECTNAME)/templates
SUBDIRS=
TEMPLATES=$(wildcard *.html)

all: subdirs

install: create_dir install_templates install_subdirs

clean: clean_subdirs
	rm -f *~

include $(TOP_DIR)/targets.mk
