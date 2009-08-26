TOP_DIR=..

include $(TOP_DIR)/config.mk

CURRENT_INSTALL_DIR=$(INSTALL_DJANGO_DIR)/$(PROJECTNAME)/pics
FILES=$(wildcard *.png) $(wildcard *.gif)

all:

install: create_dir install_files

clean:
	rm -f *~

include $(TOP_DIR)/targets.mk
