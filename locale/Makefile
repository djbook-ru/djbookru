TOP_DIR=..

include $(TOP_DIR)/config.mk

CURRENT_INSTALL_DIR=$(INSTALL_DJANGO_DIR)/$(PROJECTNAME)/locale
SUBDIRS=ru

all: subdirs

install: create_dir install_subdirs

clean: clean_subdirs
	rm -f *~

include $(TOP_DIR)/targets.mk
