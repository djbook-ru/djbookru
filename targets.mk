#
# Действия
# $Id$
#

MAKE=`which make`

subdirs:
	for i in $(SUBDIRS) end-of-subdirs-list; do \
		if [ $$i != end-of-subdirs-list ]; then \
			cd $$i; $(MAKE); cd -; \
		fi; \
	done

install_subdirs:
	for i in $(SUBDIRS) end-of-subdirs-list; do \
		if [ $$i != end-of-subdirs-list ]; then \
			cd $$i; $(MAKE) install; cd -; \
		fi; \
	done

clean_subdirs:
	for i in $(SUBDIRS) end-of-subdirs-list; do \
		if [ $$i != end-of-subdirs-list ]; then \
			cd $$i; $(MAKE) clean; cd -; \
		fi; \
	done

create_dir:
	mkdir -p $(CURRENT_INSTALL_DIR);

install_files:
	cp $(FILES) $(CURRENT_INSTALL_DIR)/;

install_templates:
	for i in $(TEMPLATES) end-of-files-list; do \
	  if [ $$i != end-of-files-list ]; then \
	    sed 's/$(REGEXP_DEVEL_URL)/\//' < $$i > $(CURRENT_INSTALL_DIR)/$$i; \
	  fi; \
	done

chown_all:
	chown -R $(OWNER):$(GROUP) $(CURRENT_INSTALL_DIR);

